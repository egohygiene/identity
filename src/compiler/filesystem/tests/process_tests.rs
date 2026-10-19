// Copyright 2026 Ego Hygiene
// SPDX-License-Identifier: MIT

use std::io::{BufRead, BufReader};
use std::process::{Child, Command, ExitStatus, Stdio};
use std::sync::mpsc::{self, Receiver};
use std::time::{Duration, Instant};

use super::*;

const WORKER: &str = "compiler::filesystem::tests::process_tests::worker";
const READY: &str = "IDENTITY_PROCESS_READY";
const LOCK: &str = ".cache/identity/writer.lock";
const PROCESS_TIMEOUT: Duration = Duration::from_secs(30);

fn snapshot(root: &Path) -> BTreeMap<PathBuf, Vec<u8>> {
    tree_with_writer_lock_metadata(root, cfg!(windows))
}

#[derive(Deserialize, Serialize)]
struct Request {
    root: PathBuf,
    output_root: String,
    operation: Operation,
    checkpoint: Option<usize>,
}

#[derive(Deserialize, Serialize)]
enum Operation {
    Commit {
        plan: Box<CompilerPlan>,
        artifacts: Vec<(String, String, Vec<u8>)>,
        manifest: Box<CompilerManifest>,
    },
    Recover,
}

#[derive(Debug, Deserialize, Serialize)]
enum Response {
    Committed,
    Recovered(RecoveryReport),
    Failed(CompilerError),
}

fn commit_request(
    root: &Path,
    fixture: &(CompilerPlan, Vec<RenderedArtifact>, CompilerManifest),
    checkpoint: Option<usize>,
) -> Request {
    Request {
        root: root.to_path_buf(),
        output_root: fixture.0.output_root.clone(),
        operation: Operation::Commit {
            plan: Box::new(fixture.0.clone()),
            artifacts: fixture
                .1
                .iter()
                .map(|artifact| {
                    (
                        artifact.target_id.clone(),
                        artifact.path.clone(),
                        artifact.bytes.clone(),
                    )
                })
                .collect(),
            manifest: Box::new(fixture.2.clone()),
        },
        checkpoint,
    }
}

fn recover_request(root: &Path, output_root: &str, checkpoint: Option<usize>) -> Request {
    Request {
        root: root.to_path_buf(),
        output_root: output_root.to_owned(),
        operation: Operation::Recover,
        checkpoint,
    }
}

// The parent supplies an exact test filter. Normal test discovery never executes
// this worker, and requests/results remain outside the consumer repository.
#[test]
#[ignore = "independent process helper; invoked only by the bounded process tests"]
fn worker() {
    let request_path = std::env::var_os("IDENTITY_PROCESS_REQUEST").unwrap();
    let response_path = std::env::var_os("IDENTITY_PROCESS_RESPONSE").unwrap();
    let request: Request = serde_json::from_slice(&fs::read(request_path).unwrap()).unwrap();
    let mut store =
        LocalArtifactStore::with_output_root(&request.root, &request.output_root).unwrap();
    if let Some(checkpoint) = request.checkpoint {
        store = store.pause_at(if checkpoint == 0 {
            TestCheckpoint::WriterLocked
        } else {
            TestCheckpoint::Mutation(checkpoint)
        });
    }
    let response = match request.operation {
        Operation::Commit {
            plan,
            artifacts,
            manifest,
        } => {
            let artifacts = artifacts
                .into_iter()
                .map(|(target_id, path, bytes)| RenderedArtifact {
                    target_id,
                    path,
                    bytes,
                })
                .collect::<Vec<_>>();
            match store.commit(&plan, &artifacts, &manifest) {
                Ok(()) => Response::Committed,
                Err(error) => Response::Failed(error),
            }
        }
        Operation::Recover => match store.recover() {
            Ok(report) => Response::Recovered(report),
            Err(error) => Response::Failed(error),
        },
    };
    fs::write(response_path, serde_json::to_vec(&response).unwrap()).unwrap();
}

struct Worker {
    child: Child,
    lines: Receiver<String>,
    response_path: PathBuf,
    _transport: TempDir,
}

impl Worker {
    fn start(request: &Request) -> Self {
        let transport = TempDir::new().unwrap();
        let request_path = transport.path().join("request.json");
        let response_path = transport.path().join("response.json");
        fs::write(&request_path, serde_json::to_vec(request).unwrap()).unwrap();
        let mut child = Command::new(std::env::current_exe().unwrap())
            .args([
                "--exact",
                WORKER,
                "--ignored",
                "--nocapture",
                "--test-threads=1",
            ])
            .env("IDENTITY_PROCESS_REQUEST", request_path)
            .env("IDENTITY_PROCESS_RESPONSE", &response_path)
            .stdin(Stdio::piped())
            .stdout(Stdio::piped())
            .stderr(Stdio::inherit())
            .spawn()
            .unwrap();
        let stdout = child.stdout.take().unwrap();
        let (sender, lines) = mpsc::channel();
        std::thread::spawn(move || {
            for line in BufReader::new(stdout).lines() {
                let Ok(line) = line else {
                    break;
                };
                if sender.send(line).is_err() {
                    break;
                }
            }
        });
        Self {
            child,
            lines,
            response_path,
            _transport: transport,
        }
    }

    fn ready(&mut self) {
        let started = Instant::now();
        let mut output = Vec::new();
        loop {
            let remaining = PROCESS_TIMEOUT.saturating_sub(started.elapsed());
            let line = self.lines.recv_timeout(remaining).unwrap_or_else(|error| {
                panic!("worker did not reach barrier: {error}; {output:?}")
            });
            let ready = line.contains(READY);
            output.push(line);
            if ready {
                assert!(self.child.try_wait().unwrap().is_none());
                return;
            }
        }
    }

    fn release(&mut self) {
        self.child.stdin.as_mut().unwrap().write_all(b"\n").unwrap();
    }

    fn wait_status(&mut self) -> ExitStatus {
        let started = Instant::now();
        loop {
            if let Some(status) = self.child.try_wait().unwrap() {
                return status;
            }
            assert!(started.elapsed() < PROCESS_TIMEOUT, "worker did not finish");
            std::thread::sleep(Duration::from_millis(10));
        }
    }

    fn finish(mut self) -> Response {
        assert!(self.wait_status().success(), "worker process failed");
        serde_json::from_slice(&fs::read(&self.response_path).unwrap()).unwrap()
    }

    fn kill(&mut self) {
        self.child.kill().unwrap();
        assert!(!self.wait_status().success(), "worker was not terminated");
        assert!(!self.response_path.exists());
    }
}

impl Drop for Worker {
    fn drop(&mut self) {
        // Release the OS guard even if a parent assertion or timeout panics.
        let _ = self.child.kill();
        let _ = self.child.wait();
    }
}

fn run(request: &Request) -> Response {
    Worker::start(request).finish()
}

fn assert_busy(request: &Request) {
    let before = snapshot(&request.root);
    match run(request) {
        Response::Failed(error) => {
            assert_eq!(error.kind, FailureKind::Blocked, "{error:?}");
            assert_eq!(error.diagnostics[0].code, "IDN2346", "{error:?}");
        }
        response => panic!("another process bypassed the writer lock: {response:?}"),
    }
    assert_eq!(
        snapshot(&request.root),
        before,
        "contender changed repository state"
    );
}

fn assert_recovered(response: Response, count: u64) {
    match response {
        Response::Recovered(report) => assert_eq!(report.recovered_transactions, count),
        response => panic!("expected recovery, got {response:?}"),
    }
}

fn assert_original_outputs(root: &Path, output_root: &str) {
    assert!(!root.join(output_root).join("created.json").exists());
    for (relative, expected) in [
        ("replaced.json", b"old replaced".as_slice()),
        ("removed.json", b"old removed".as_slice()),
        (".identity-manifest.json", b"old manifest".as_slice()),
    ] {
        assert_eq!(
            fs::read(root.join(output_root).join(relative)).unwrap(),
            expected
        );
    }
    assert_eq!(
        fs::read(root.join(".identity/sentinel")).unwrap(),
        b"canonical sentinel"
    );
}

#[test]
fn empty_recovery_creates_only_reusable_persistent_coordination_metadata() {
    let root = TempDir::new().unwrap();
    write_fixture(
        &root.path().join(".identity/sentinel"),
        b"canonical sentinel",
    )
    .unwrap();
    let mut expected = tree(root.path());
    for relative in [".cache", ".cache/identity", LOCK] {
        expected.insert(PathBuf::from(relative), Vec::new());
    }
    assert_recovered(run(&recover_request(root.path(), OUTPUT, None)), 0);
    assert_eq!(tree(root.path()), expected);
    assert_recovered(run(&recover_request(root.path(), OUTPUT, None)), 0);
    assert_eq!(tree(root.path()), expected);
    assert!(
        !LocalArtifactStore::new(root.path())
            .unwrap()
            .recovery_required()
            .unwrap()
    );
}

#[test]
fn active_generation_blocks_independent_writers_for_every_plan_and_output_root() {
    let root = TempDir::new().unwrap();
    let baseline = fixture(root.path(), OUTPUT);
    let custom = fixture(root.path(), "generated/branding");
    let mut changed = baseline.clone();
    changed.0.source_digest = "b".repeat(64);
    changed.0.plan_digest = crate::compiler::plan_digest(&changed.0).unwrap();
    changed.2.source_digest.clone_from(&changed.0.source_digest);
    changed.2.plan_digest.clone_from(&changed.0.plan_digest);
    assert_ne!(baseline.0.plan_digest, changed.0.plan_digest);

    let mut owner = Worker::start(&commit_request(root.path(), &baseline, Some(0)));
    owner.ready();
    let before = snapshot(root.path());
    for request in [
        commit_request(root.path(), &baseline, None),
        commit_request(root.path(), &changed, None),
        commit_request(root.path(), &custom, None),
        recover_request(root.path(), OUTPUT, None),
        recover_request(root.path(), "generated/branding", None),
    ] {
        assert_busy(&request);
        assert_eq!(snapshot(root.path()), before);
    }
    #[cfg(unix)]
    {
        let aliases = TempDir::new().unwrap();
        let alias = aliases.path().join("same-repository");
        std::os::unix::fs::symlink(root.path(), &alias).unwrap();
        assert_busy(&commit_request(&alias, &baseline, None));
    }
    owner.release();
    assert!(matches!(owner.finish(), Response::Committed));
    assert_eq!(fs::read(root.path().join(LOCK)).unwrap(), b"");
    let committed = tree(root.path());
    match run(&commit_request(root.path(), &baseline, None)) {
        Response::Failed(error) => {
            assert_eq!(error.kind, FailureKind::Drifted);
            assert_eq!(error.diagnostics[0].code, "IDN2308");
        }
        response => panic!("stale plan bypassed current-state checks: {response:?}"),
    }
    assert_eq!(tree(root.path()), committed);
    assert!(matches!(
        run(&commit_request(root.path(), &custom, None)),
        Response::Committed
    ));
    assert_recovered(run(&recover_request(root.path(), OUTPUT, None)), 0);
}

#[test]
fn active_recovery_blocks_independent_generation_and_other_recovery() {
    let root = TempDir::new().unwrap();
    let baseline = fixture(root.path(), OUTPUT);
    let custom = fixture(root.path(), "generated/branding");
    write_fixture(
        &root.path().join(".identity/sentinel"),
        b"canonical sentinel",
    )
    .unwrap();
    interrupted(root.path(), OUTPUT, 4);
    let mut owner = Worker::start(&recover_request(root.path(), OUTPUT, Some(0)));
    owner.ready();
    for request in [
        commit_request(root.path(), &baseline, None),
        commit_request(root.path(), &custom, None),
        recover_request(root.path(), OUTPUT, None),
        recover_request(root.path(), "generated/branding", None),
    ] {
        assert_busy(&request);
    }
    owner.release();
    assert_recovered(owner.finish(), 1);
    assert_original_outputs(root.path(), OUTPUT);
    assert_recovered(run(&recover_request(root.path(), OUTPUT, None)), 0);
}

#[test]
fn no_op_commit_holds_the_same_writer_lock_and_leaves_every_byte_unchanged() {
    let root = TempDir::new().unwrap();
    let baseline = fixture(root.path(), OUTPUT);
    assert!(matches!(
        run(&commit_request(root.path(), &baseline, None)),
        Response::Committed
    ));
    let mut no_op = baseline;
    no_op
        .0
        .actions
        .retain(|action| action.operation != PlanOperation::Remove);
    for action in &mut no_op.0.actions {
        let bytes = fs::read(root.path().join(&action.path)).unwrap();
        action.operation = PlanOperation::Unchanged;
        action.current_sha256 = Some(sha256_hex(&bytes));
        action.current_bytes = Some(u64::try_from(bytes.len()).unwrap());
    }
    no_op.0.plan_digest = crate::compiler::plan_digest(&no_op.0).unwrap();
    no_op.1.clear();
    assert!(!no_op.0.has_mutations());
    let before = snapshot(root.path());
    let mut owner = Worker::start(&commit_request(root.path(), &no_op, Some(0)));
    owner.ready();
    assert_eq!(snapshot(root.path()), before);
    assert_busy(&commit_request(root.path(), &no_op, None));
    assert_busy(&recover_request(root.path(), OUTPUT, None));
    owner.release();
    assert!(matches!(owner.finish(), Response::Committed));
    assert_eq!(snapshot(root.path()), before);
    assert_eq!(fs::read(root.path().join(LOCK)).unwrap(), b"");
    assert!(
        !LocalArtifactStore::new(root.path())
            .unwrap()
            .recovery_required()
            .unwrap()
    );
}

#[test]
fn killing_generation_releases_the_lock_without_discarding_its_original_journal() {
    let root = TempDir::new().unwrap();
    let baseline = fixture(root.path(), OUTPUT);
    write_fixture(
        &root.path().join(".identity/sentinel"),
        b"canonical sentinel",
    )
    .unwrap();
    let mut owner = Worker::start(&commit_request(root.path(), &baseline, Some(1)));
    owner.ready();
    let journal_path = root
        .path()
        .join(TRANSACTION_ROOT)
        .join(&baseline.0.plan_digest)
        .join("journal.json");
    let original_journal = fs::read(&journal_path).unwrap();
    assert_eq!(
        fs::read(root.path().join(OUTPUT).join("created.json")).unwrap(),
        b"new created.json"
    );
    assert_busy(&commit_request(root.path(), &baseline, None));
    assert_busy(&recover_request(root.path(), OUTPUT, None));
    let before_kill = snapshot(root.path());
    owner.kill();
    assert_eq!(snapshot(root.path()), before_kill);
    match run(&commit_request(root.path(), &baseline, None)) {
        Response::Failed(error) => assert_eq!(error.diagnostics[0].code, "IDN2301"),
        response => panic!("pending journal was bypassed after owner exit: {response:?}"),
    }
    assert_eq!(snapshot(root.path()), before_kill);
    assert_eq!(fs::read(&journal_path).unwrap(), original_journal);
    assert_recovered(run(&recover_request(root.path(), OUTPUT, None)), 1);
    assert_original_outputs(root.path(), OUTPUT);
    let recovered = snapshot(root.path());
    assert_recovered(run(&recover_request(root.path(), OUTPUT, None)), 0);
    assert_eq!(snapshot(root.path()), recovered);
    assert_eq!(fs::read(root.path().join(LOCK)).unwrap(), b"");
    assert!(matches!(
        run(&commit_request(root.path(), &baseline, None)),
        Response::Committed
    ));
}

#[test]
fn killing_recovery_releases_the_lock_and_allows_repeating_original_rollback() {
    let root = TempDir::new().unwrap();
    let baseline = fixture(root.path(), OUTPUT);
    write_fixture(
        &root.path().join(".identity/sentinel"),
        b"canonical sentinel",
    )
    .unwrap();
    let transaction = interrupted(root.path(), OUTPUT, 4);
    let original_journal = fs::read(transaction.join("journal.json")).unwrap();
    let mut owner = Worker::start(&recover_request(root.path(), OUTPUT, Some(1)));
    owner.ready();
    assert_busy(&commit_request(root.path(), &baseline, None));
    assert_busy(&recover_request(root.path(), OUTPUT, None));
    let before_kill = snapshot(root.path());
    owner.kill();
    assert_eq!(snapshot(root.path()), before_kill);
    assert_eq!(
        fs::read(transaction.join("journal.json")).unwrap(),
        original_journal
    );
    assert_recovered(run(&recover_request(root.path(), OUTPUT, None)), 1);
    assert_original_outputs(root.path(), OUTPUT);
    let recovered = snapshot(root.path());
    assert_recovered(run(&recover_request(root.path(), OUTPUT, None)), 0);
    assert_eq!(snapshot(root.path()), recovered);
    assert_eq!(fs::read(root.path().join(LOCK)).unwrap(), b"");
    assert!(matches!(
        run(&commit_request(root.path(), &baseline, None)),
        Response::Committed
    ));
}

#[test]
fn persistent_hard_linked_lock_files_are_never_truncated_replaced_or_deleted() {
    let root = TempDir::new().unwrap();
    let alias_root = TempDir::new().unwrap();
    let baseline = fixture(root.path(), OUTPUT);
    let alias_fixture = fixture(alias_root.path(), OUTPUT);
    let evidence = b"preexisting coordination evidence";
    write_fixture(&root.path().join(LOCK), evidence).unwrap();
    fs::create_dir_all(alias_root.path().join(".cache").join("identity")).unwrap();
    fs::hard_link(root.path().join(LOCK), alias_root.path().join(LOCK)).unwrap();
    let alias_before = snapshot(alias_root.path());
    let alias_bytes_before = tree(alias_root.path());
    let mut owner = Worker::start(&commit_request(root.path(), &baseline, Some(0)));
    owner.ready();
    assert_busy(&commit_request(root.path(), &baseline, None));
    assert_busy(&commit_request(alias_root.path(), &alias_fixture, None));
    assert_eq!(snapshot(alias_root.path()), alias_before);
    owner.release();
    assert!(matches!(owner.finish(), Response::Committed));
    assert_eq!(tree(alias_root.path()), alias_bytes_before);
    assert_eq!(fs::read(alias_root.path().join(LOCK)).unwrap(), evidence);
    assert!(matches!(
        run(&commit_request(alias_root.path(), &alias_fixture, None)),
        Response::Committed
    ));
    for repository in [root.path(), alias_root.path()] {
        assert_eq!(fs::read(repository.join(LOCK)).unwrap(), evidence);
        assert_recovered(run(&recover_request(repository, OUTPUT, None)), 0);
        assert_eq!(fs::read(repository.join(LOCK)).unwrap(), evidence);
    }
}

#[test]
fn a_directory_at_the_lock_path_is_preserved_and_rejected_by_both_operations() {
    let root = TempDir::new().unwrap();
    let baseline = fixture(root.path(), OUTPUT);
    fs::create_dir_all(root.path().join(LOCK)).unwrap();
    write_fixture(
        &root.path().join(LOCK).join("sentinel"),
        b"preserve directory",
    )
    .unwrap();
    let before = snapshot(root.path());
    for request in [
        commit_request(root.path(), &baseline, None),
        recover_request(root.path(), OUTPUT, None),
    ] {
        assert!(matches!(run(&request), Response::Failed(_)));
        assert_eq!(snapshot(root.path()), before);
    }
}

#[cfg(unix)]
#[test]
fn redirected_lock_files_preserve_the_repository_and_external_target() {
    for dangling in [false, true] {
        let root = TempDir::new().unwrap();
        let external = TempDir::new().unwrap();
        let baseline = fixture(root.path(), OUTPUT);
        let target = external.path().join("lock-target");
        if !dangling {
            write_fixture(&target, b"external evidence").unwrap();
        }
        fs::create_dir_all(root.path().join(".cache").join("identity")).unwrap();
        std::os::unix::fs::symlink(&target, root.path().join(LOCK)).unwrap();
        let before = snapshot(root.path());
        let external_before = snapshot(external.path());
        for request in [
            commit_request(root.path(), &baseline, None),
            recover_request(root.path(), OUTPUT, None),
        ] {
            assert!(matches!(run(&request), Response::Failed(_)));
            assert_eq!(snapshot(root.path()), before);
            assert_eq!(snapshot(external.path()), external_before);
        }
    }
}

#[cfg(unix)]
#[test]
fn a_fifo_at_the_lock_path_is_rejected_without_opening_or_changing_it() {
    let root = TempDir::new().unwrap();
    let baseline = fixture(root.path(), OUTPUT);
    fs::create_dir_all(root.path().join(".cache").join("identity")).unwrap();
    let status = Command::new("mkfifo")
        .arg(root.path().join(LOCK))
        .status()
        .unwrap();
    assert!(status.success());
    let before = tree(root.path());
    for request in [
        commit_request(root.path(), &baseline, None),
        recover_request(root.path(), OUTPUT, None),
    ] {
        assert!(matches!(run(&request), Response::Failed(_)));
        assert_eq!(tree(root.path()), before);
    }
}

#[cfg(windows)]
#[test]
fn junction_lock_paths_preserve_the_repository_and_external_target() {
    let root = TempDir::new().unwrap();
    let external = TempDir::new().unwrap();
    let baseline = fixture(root.path(), OUTPUT);
    write_fixture(&external.path().join("sentinel"), b"external evidence").unwrap();
    let lock = append_portable(root.path(), LOCK);
    fs::create_dir_all(lock.parent().unwrap()).unwrap();
    let result = Command::new("cmd")
        .args(["/C", "mklink", "/J"])
        .arg(&lock)
        .arg(external.path())
        .output()
        .unwrap();
    assert!(
        result.status.success(),
        "{}",
        String::from_utf8_lossy(&result.stderr)
    );
    let before = snapshot(root.path());
    let external_before = snapshot(external.path());
    for request in [
        commit_request(root.path(), &baseline, None),
        recover_request(root.path(), OUTPUT, None),
    ] {
        assert!(matches!(run(&request), Response::Failed(_)));
        assert_eq!(snapshot(root.path()), before);
        assert_eq!(snapshot(external.path()), external_before);
    }
}
