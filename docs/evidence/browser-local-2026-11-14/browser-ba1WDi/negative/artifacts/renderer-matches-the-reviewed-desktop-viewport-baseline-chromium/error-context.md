# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: renderer.spec.js >> matches the reviewed desktop viewport baseline
- Location: tests/e2e/renderer.spec.js:136:1

# Error details

```
Error: expect(page).toHaveScreenshot(expected) failed

  1408445 pixels (ratio 0.98 of all image pixels) are different.

  Snapshot: brand-kit-page.png

Call log:
  - Expect "toHaveScreenshot(brand-kit-page.png)" with timeout 5000ms
    - verifying given screenshot expectation
  - taking page screenshot
    - disabled all CSS animations
  - waiting for fonts to load...
  - fonts loaded
  - 1408445 pixels (ratio 0.98 of all image pixels) are different.
  - waiting 100ms before taking screenshot
  - taking page screenshot
    - disabled all CSS animations
  - waiting for fonts to load...
  - fonts loaded
  - captured a stable screenshot
  - 1408445 pixels (ratio 0.98 of all image pixels) are different.

```

# Page snapshot

```yaml
- generic [ref=f1e3]:
  - link "Skip to Brand Kit content" [ref=f1e4] [cursor=pointer]:
    - /url: "#main-content"
  - banner [ref=f1e5]:
    - generic [ref=f1e6]:
      - paragraph [ref=f1e7]: Public Brand Kit
      - heading "Example Product" [level=1] [ref=f1e8]
      - paragraph [ref=f1e9]: A governed reference-renderer fixture.
      - generic [ref=f1e10]:
        - generic [ref=f1e11]: Release 1.0.0
        - generic [ref=f1e12]: generated
    - generic [ref=f1e13]:
      - button "Change color theme" [ref=f1e14] [cursor=pointer]: "Theme: system"
      - link "Download complete kit" [ref=f1e15] [cursor=pointer]:
        - /url: ./packages/brand-kit/brand-kit.zip
  - generic [ref=f1e16]:
    - complementary [ref=f1e17]:
      - navigation "Brand Kit sections" [ref=f1e18]:
        - list [ref=f1e19]:
          - listitem [ref=f1e20]:
            - link "Overview" [ref=f1e21] [cursor=pointer]:
              - /url: "#overview"
          - listitem [ref=f1e22]:
            - link "Logos and marks" [ref=f1e23] [cursor=pointer]:
              - /url: "#logos"
          - listitem [ref=f1e24]:
            - link "Color palette" [ref=f1e25] [cursor=pointer]:
              - /url: "#colors"
          - listitem [ref=f1e26]:
            - link "Typography" [ref=f1e27] [cursor=pointer]:
              - /url: "#typography"
          - listitem [ref=f1e28]:
            - link "Voice and personality" [ref=f1e29] [cursor=pointer]:
              - /url: "#voice"
          - listitem [ref=f1e30]:
            - link "Usage rules" [ref=f1e31] [cursor=pointer]:
              - /url: "#usage"
          - listitem [ref=f1e32]:
            - link "Motion, imagery, and mascot" [ref=f1e33] [cursor=pointer]:
              - /url: "#creative-direction"
          - listitem [ref=f1e34]:
            - link "Review candidate assets" [ref=f1e35] [cursor=pointer]:
              - /url: "#studio"
          - listitem [ref=f1e36]:
            - link "Downloads" [ref=f1e37] [cursor=pointer]:
              - /url: "#downloads"
          - listitem [ref=f1e38]:
            - link "Provenance and support" [ref=f1e39] [cursor=pointer]:
              - /url: "#provenance"
    - main [ref=f1e40]:
      - region [ref=f1e41]:
        - heading "Overview and version" [level=2] [ref=f1e43]
        - generic [ref=f1e44]:
          - article [ref=f1e45]:
            - paragraph [ref=f1e46]: Immutable release
            - heading "Example Product" [level=3] [ref=f1e47]
            - paragraph [ref=f1e48]: A governed reference-renderer fixture.
            - generic [ref=f1e49]:
              - term [ref=f1e50]: Version
              - definition [ref=f1e51]: 1.0.0
              - term [ref=f1e52]: Profile
              - definition [ref=f1e53]: 1.0.0
              - term [ref=f1e54]: Status
              - definition [ref=f1e55]: generated
              - term [ref=f1e56]: Immutable ID
              - definition [ref=f1e57]:
                - code [ref=f1e58]: sha256:545e54ad462fa84807ef594110a6742bf861bdf90a7e71fd60e1729b05d58516
          - article [ref=f1e59]:
            - paragraph [ref=f1e60]: Authority boundary
            - heading "What this page represents" [level=3] [ref=f1e61]
            - paragraph [ref=f1e62]: Assets and previews are generated projections. Voice and usage sections are labeled separately because they project canonical, human-reviewed guidance.
      - region [ref=f1e63]:
        - generic [ref=f1e64]:
          - heading "Logo and marks" [level=2] [ref=f1e65]
          - generic [ref=f1e66]: Generated preview
        - article [ref=f1e68]:
          - img "A violet diamond nested inside a rounded square." [ref=f1e70]
          - heading "Mark" [level=3] [ref=f1e71]
          - generic [ref=f1e72]:
            - term [ref=f1e73]: Format
            - definition [ref=f1e74]: image/svg+xml
            - term [ref=f1e75]: Dimensions
            - definition [ref=f1e76]: 64 × 64 SVG viewBox units
            - term [ref=f1e77]: Intended use
            - definition [ref=f1e78]: Primary scalable brand mark for approved product surfaces.
            - term [ref=f1e79]: Availability
            - definition [ref=f1e80]: Generated Download
            - term [ref=f1e81]: SHA-256
            - definition [ref=f1e82]:
              - code [ref=f1e83]: e35e3b2ab6ae457e3b7a2522e81142d26031e526de06c6bd541b1c97208e3f4b
            - term [ref=f1e84]: Safe zone
            - definition [ref=f1e85]: 54%
            - term [ref=f1e86]: License
            - definition [ref=f1e87]: MIT · approved
          - link "Download Mark" [ref=f1e88] [cursor=pointer]:
            - /url: ./brand/mark.svg
      - region [ref=f1e89]:
        - generic [ref=f1e90]:
          - heading "Color palette and approved pairings" [level=2] [ref=f1e91]
          - generic [ref=f1e92]: Generated preview
        - generic [ref=f1e93]:
          - generic [ref=f1e94]:
            - article [ref=f1e95]:
              - 'img "color.brand.primary previewed as #6b33b8" [ref=f1e96]'
              - heading "color.brand.primary" [level=3] [ref=f1e97]
              - paragraph [ref=f1e98]: "#6b33b8"
              - button "Copy value" [ref=f1e99] [cursor=pointer]
              - paragraph [ref=f1e100]: "Source layer: example-product"
            - article [ref=f1e101]:
              - 'img "color.brand.secondary previewed as #2ea37a" [ref=f1e102]'
              - heading "color.brand.secondary" [level=3] [ref=f1e103]
              - paragraph [ref=f1e104]: "#2ea37a"
              - button "Copy value" [ref=f1e105] [cursor=pointer]
              - paragraph [ref=f1e106]: "Source layer: example-product"
            - article [ref=f1e107]:
              - 'img "color.canvas previewed as #fafaff" [ref=f1e108]'
              - heading "color.canvas" [level=3] [ref=f1e109]
              - paragraph [ref=f1e110]: "#fafaff"
              - button "Copy value" [ref=f1e111] [cursor=pointer]
              - paragraph [ref=f1e112]: "Source layer: example-organization"
            - article [ref=f1e113]:
              - 'img "color.surface previewed as #ffffff" [ref=f1e114]'
              - heading "color.surface" [level=3] [ref=f1e115]
              - paragraph [ref=f1e116]: "#ffffff"
              - button "Copy value" [ref=f1e117] [cursor=pointer]
              - paragraph [ref=f1e118]: "Source layer: example-organization"
            - article [ref=f1e119]:
              - 'img "color.text previewed as #0d0f1a" [ref=f1e120]'
              - heading "color.text" [level=3] [ref=f1e121]
              - paragraph [ref=f1e122]: "#0d0f1a"
              - button "Copy value" [ref=f1e123] [cursor=pointer]
              - paragraph [ref=f1e124]: "Source layer: example-organization"
            - article [ref=f1e125]:
              - 'img "color.text.muted previewed as #595e70" [ref=f1e126]'
              - heading "color.text.muted" [level=3] [ref=f1e127]
              - paragraph [ref=f1e128]: "#595e70"
              - button "Copy value" [ref=f1e129] [cursor=pointer]
              - paragraph [ref=f1e130]: "Source layer: example-organization"
            - article [ref=f1e131]:
              - 'img "color.border previewed as #d1d1e0" [ref=f1e132]'
              - heading "color.border" [level=3] [ref=f1e133]
              - paragraph [ref=f1e134]: "#d1d1e0"
              - button "Copy value" [ref=f1e135] [cursor=pointer]
              - paragraph [ref=f1e136]: "Source layer: example-organization"
          - note [ref=f1e137]:
            - heading "Approved pairings not declared" [level=3] [ref=f1e138]
            - paragraph [ref=f1e139]: Semantic colors are previewed individually, but the current release does not declare canonical color pairings. The renderer does not infer combinations.
      - region [ref=f1e140]:
        - generic [ref=f1e141]:
          - heading "Typography and type scale" [level=2] [ref=f1e142]
          - generic [ref=f1e143]: Generated preview
        - generic [ref=f1e144]:
          - generic [ref=f1e145]:
            - article [ref=f1e146]:
              - paragraph [ref=f1e147]: typography.body.family
              - paragraph [ref=f1e148]: Clarity makes a system easier to trust.
              - paragraph [ref=f1e149]: Inter, system-ui, sans-serif
              - button "Copy value" [ref=f1e150] [cursor=pointer]
            - article [ref=f1e151]:
              - paragraph [ref=f1e152]: typography.heading.family
              - paragraph [ref=f1e153]: Clarity makes a system easier to trust.
              - paragraph [ref=f1e154]: Inter, system-ui, sans-serif
              - button "Copy value" [ref=f1e155] [cursor=pointer]
          - note [ref=f1e156]:
            - heading "Type scale not declared" [level=3] [ref=f1e157]
            - paragraph [ref=f1e158]: Font family tokens are available, but the current release does not declare canonical sizes, weights, or line-height relationships.
      - region [ref=f1e159]:
        - generic [ref=f1e160]:
          - heading "Voice and personality" [level=2] [ref=f1e161]
          - generic [ref=f1e162]: Canonical guidance
        - generic [ref=f1e163]:
          - article [ref=f1e164]:
            - heading "Personality" [level=3] [ref=f1e165]
            - list [ref=f1e166]:
              - listitem [ref=f1e167]: clear
              - listitem [ref=f1e168]: warm
              - listitem [ref=f1e169]: grounded
          - article [ref=f1e170]:
            - heading "Principles" [level=3] [ref=f1e171]
            - list [ref=f1e172]:
              - listitem [ref=f1e173]: Explain the reason before the mechanism.
              - listitem [ref=f1e174]: Prefer direct language over performance.
          - article [ref=f1e175]:
            - heading "Avoid" [level=3] [ref=f1e176]
            - list [ref=f1e177]:
              - listitem [ref=f1e178]: Manufactured urgency
              - listitem [ref=f1e179]: Unreviewed claims
      - region [ref=f1e180]:
        - generic [ref=f1e181]:
          - heading "Usage rules" [level=2] [ref=f1e182]
          - generic [ref=f1e183]: Canonical guidance
        - generic [ref=f1e184]:
          - article [ref=f1e185]:
            - heading "Do" [level=3] [ref=f1e186]
            - list [ref=f1e187]:
              - listitem [ref=f1e188]: Use semantic tokens instead of copied color values.
              - listitem [ref=f1e189]: Preserve clear space around the mark.
          - article [ref=f1e190]:
            - heading "Dont" [level=3] [ref=f1e191]
            - list [ref=f1e192]:
              - listitem [ref=f1e193]: Stretch or recolor approved marks.
              - listitem [ref=f1e194]: Present generated previews as canonical guidance.
      - region [ref=f1e195]:
        - heading "Motion, imagery, and mascot guidance" [level=2] [ref=f1e197]
        - generic [ref=f1e198]:
          - article [ref=f1e199]:
            - heading "Motion" [level=3] [ref=f1e200]
            - paragraph [ref=f1e201]: Declared
            - paragraph [ref=f1e202]: The release contains structured source data for this area.
          - article [ref=f1e203]:
            - heading "Imagery" [level=3] [ref=f1e204]
            - paragraph [ref=f1e205]: Not declared
            - paragraph [ref=f1e206]: No canonical guidance is declared; the renderer leaves this area explicit rather than fabricating examples.
          - article [ref=f1e207]:
            - heading "Mascot" [level=3] [ref=f1e208]
            - paragraph [ref=f1e209]: Not declared
            - paragraph [ref=f1e210]: No canonical guidance is declared; the renderer leaves this area explicit rather than fabricating examples.
      - region [ref=f1e211]:
        - heading "Review candidate assets" [level=2] [ref=f1e213]
        - generic [ref=f1e214]:
          - paragraph [ref=f1e215]: Import a portable candidate bundle to compare local candidates against the immutable approved release. Previewing never writes canonical or generated files.
          - generic [ref=f1e216]: Import candidate bundle
          - button "Import candidate bundle" [ref=f1e217]
          - generic [ref=f1e218]: Candidate bundle JSON
          - textbox "Candidate bundle JSON" [ref=f1e219]:
            - /placeholder: "{ \"schema\": \"identity.brand-kit-candidate/v1\", \"profiles\": [\"social\"], ... }"
          - generic [ref=f1e220]:
            - button "Validate and preview plan" [ref=f1e221] [cursor=pointer]
            - button "Export review bundle" [disabled] [ref=f1e222] [cursor=pointer]
          - generic [ref=f1e223]: No candidate bundle has been loaded.
          - generic [ref=f1e224]: No candidate comparison is available.
          - generic [ref=f1e225]: Reviewer identity
          - textbox "Reviewer identity" [ref=f1e226]
          - generic [ref=f1e227]:
            - checkbox "I reviewed this plan and authorize a compiler handoff. This does not write files or publish assets." [ref=f1e228]
            - text: I reviewed this plan and authorize a compiler handoff. This does not write files or publish assets.
          - button "Export approved handoff" [disabled] [ref=f1e229] [cursor=pointer]
      - region [ref=f1e230]:
        - heading "Downloads and package installation" [level=2] [ref=f1e232]
        - generic [ref=f1e233]:
          - article [ref=f1e234]:
            - generic [ref=f1e235]:
              - heading "Complete Brand Kit" [level=3] [ref=f1e236]
              - paragraph [ref=f1e237]: Versioned offline archive of approved generated assets.
              - paragraph [ref=f1e238]: application/zip · packages/brand-kit/brand-kit.zip
            - link "Download" [ref=f1e239] [cursor=pointer]:
              - /url: ./packages/brand-kit/brand-kit.zip
          - article [ref=f1e240]:
            - generic [ref=f1e241]:
              - heading "Design tokens" [level=3] [ref=f1e242]
              - paragraph [ref=f1e243]: DTCG-compatible semantic token projection.
              - paragraph [ref=f1e244]: application/json · packages/tokens/tokens.json
            - link "Download" [ref=f1e245] [cursor=pointer]:
              - /url: ./packages/tokens/tokens.json
          - article [ref=f1e246]:
            - generic [ref=f1e247]:
              - heading "Public metadata" [level=3] [ref=f1e248]
              - paragraph [ref=f1e249]: Project metadata for public integrations.
              - paragraph [ref=f1e250]: application/json · packages/metadata/metadata.json
            - link "Download" [ref=f1e251] [cursor=pointer]:
              - /url: ./packages/metadata/metadata.json
          - article [ref=f1e252]:
            - generic [ref=f1e253]:
              - heading "Voice and usage guidance" [level=3] [ref=f1e254]
              - paragraph [ref=f1e255]: Human-readable projection of canonical guidance.
              - paragraph [ref=f1e256]: text/markdown · packages/guidance/README.md
            - link "Download" [ref=f1e257] [cursor=pointer]:
              - /url: ./packages/guidance/README.md
      - region [ref=f1e258]:
        - heading "Provenance, licenses, changelog, and support" [level=2] [ref=f1e260]
        - generic [ref=f1e261]:
          - article [ref=f1e262]:
            - heading "Release evidence" [level=3] [ref=f1e263]
            - generic [ref=f1e264]:
              - term [ref=f1e265]: Immutable ID
              - definition [ref=f1e266]:
                - code [ref=f1e267]: sha256:545e54ad462fa84807ef594110a6742bf861bdf90a7e71fd60e1729b05d58516
              - term [ref=f1e268]: Source digest
              - definition [ref=f1e269]:
                - code [ref=f1e270]: 545e54ad462fa84807ef594110a6742bf861bdf90a7e71fd60e1729b05d58516
              - term [ref=f1e271]: Release status
              - definition [ref=f1e272]: generated
              - term [ref=f1e273]: Contract
              - definition [ref=f1e274]:
                - code [ref=f1e275]: identity.brand-kit-view-model/v1
          - article [ref=f1e276]:
            - heading "Mark governance" [level=3] [ref=f1e277]
            - generic [ref=f1e278]:
              - generic [ref=f1e279]:
                - term [ref=f1e280]: Asset license
                - definition [ref=f1e281]: MIT
                - term [ref=f1e282]: License review
                - definition [ref=f1e283]: approved
                - term [ref=f1e284]: Attribution
                - definition [ref=f1e285]: Example Product contributors
                - term [ref=f1e286]: Approval
                - definition [ref=f1e287]: approve-example-mark
                - term [ref=f1e288]: Creator
                - definition [ref=f1e289]: Example Product design team
                - term [ref=f1e290]: Method
                - definition [ref=f1e291]: vector
                - term [ref=f1e292]: Source
                - definition [ref=f1e293]: .identity/sources/mark.svg
                - term [ref=f1e294]: Captured
                - definition [ref=f1e295]: 2026-08-20
                - term [ref=f1e296]: SHA-256
                - definition [ref=f1e297]:
                  - code [ref=f1e298]: e35e3b2ab6ae457e3b7a2522e81142d26031e526de06c6bd541b1c97208e3f4b
                - term [ref=f1e299]: Safe zone
                - definition [ref=f1e300]: Not declared
                - term [ref=f1e301]: Minimum size
                - definition [ref=f1e302]: Not declared
              - heading "Usage restrictions" [level=4] [ref=f1e303]
              - paragraph [ref=f1e304]: No restrictions declared.
          - article [ref=f1e305]:
            - heading "Changelog and support" [level=3] [ref=f1e306]
            - paragraph [ref=f1e307]: The immutable release ID is the comparison boundary for changelog entries. Support status is represented by explicit declared, not-declared, and unsupported states throughout this page.
            - link "Review source and release history" [ref=f1e308] [cursor=pointer]:
              - /url: https://example.invalid/example-product
  - contentinfo [ref=f1e309]:
    - paragraph [ref=f1e310]: Generated from an immutable Identity view model. Canonical source remains consumer-owned.
    - link "Project repository" [ref=f1e311] [cursor=pointer]:
      - /url: https://example.invalid/example-product
  - status [ref=f1e312]: Copy controls are ready.
```

# Test source

```ts
  40  |   await expect(page).toHaveURL(/#colors$/u);
  41  |   await expect(
  42  |     page.getByRole("heading", {
  43  |       level: 2,
  44  |       name: "Color palette and approved pairings",
  45  |     }),
  46  |   ).toBeInViewport();
  47  | });
  48  | 
  49  | test("copy feedback and theme controls remain keyboard operable", async ({
  50  |   page,
  51  | }) => {
  52  |   const copyButton = page.getByRole("button", { name: "Copy value" }).first();
  53  |   await copyButton.focus();
  54  |   await expect(copyButton).toBeFocused();
  55  |   await copyButton.press("Enter");
  56  |   await expect(page.getByRole("status")).toContainText("copied");
  57  | 
  58  |   const themeButton = page.getByRole("button", { name: /Change color theme/u });
  59  |   await themeButton.focus();
  60  |   await themeButton.press("Enter");
  61  |   await expect(page.locator("html")).toHaveAttribute("data-theme", "light");
  62  |   await themeButton.press("Enter");
  63  |   await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  64  | });
  65  | 
  66  | test("studio imports a local review bundle without mutating the release", async ({ page }) => {
  67  |   const candidateBundle = {
  68  |     schema: "identity.brand-kit-candidate/v1",
  69  |     projectId: "example-product",
  70  |     sourceDigest: "545e54ad462fa84807ef594110a6742bf861bdf90a7e71fd60e1729b05d58516",
  71  |     profiles: ["social", "pwa"],
  72  |     candidates: [{
  73  |       id: "candidate-mark",
  74  |       kind: "mark",
  75  |       state: "candidate",
  76  |       provenance: { source: "local-review" },
  77  |       approvedAssetId: "mark",
  78  |     }],
  79  |   };
  80  |   await page.getByLabel("Candidate bundle JSON").fill(JSON.stringify(candidateBundle));
  81  |   await page.getByRole("button", { name: "Validate and preview plan" }).click();
  82  |   await expect(page.getByText("Candidate review · pwa, social")).toBeVisible();
  83  |   await expect(page.getByText("State: candidate. Kind: mark.")).toBeVisible();
  84  |   await expect(page.getByRole("button", { name: "Export review bundle" })).toBeEnabled();
  85  |   await page.getByLabel("Reviewer identity").fill("local reviewer");
  86  |   await page.getByLabel(/I reviewed this plan/u).check();
  87  |   await expect(page.getByRole("button", { name: "Export approved handoff" })).toBeEnabled();
  88  | });
  89  | 
  90  | test("studio preserves historical review records without staging them", async ({ page }) => {
  91  |   const candidateBundle = {
  92  |     schema: "identity.brand-kit-candidate/v1",
  93  |     projectId: "example-product",
  94  |     sourceDigest: "545e54ad462fa84807ef594110a6742bf861bdf90a7e71fd60e1729b05d58516",
  95  |     profiles: ["pwa"],
  96  |     candidates: [{
  97  |       id: "rejected-mark",
  98  |       kind: "mark",
  99  |       state: "rejected",
  100 |       provenance: { source: "local-review" },
  101 |       approvedAssetId: "mark",
  102 |     }],
  103 |   };
  104 |   await page.getByLabel("Candidate bundle JSON").fill(JSON.stringify(candidateBundle));
  105 |   await page.getByRole("button", { name: "Validate and preview plan" }).click();
  106 |   await page.getByLabel("Reviewer identity").fill("local reviewer");
  107 |   await page.getByLabel(/I reviewed this plan/u).check();
  108 |   await expect(page.getByRole("button", { name: "Export review bundle" })).toBeEnabled();
  109 |   await expect(page.getByRole("button", { name: "Export approved handoff" })).toBeDisabled();
  110 | });
  111 | 
  112 | test("honors reduced motion and remains responsive on a narrow viewport", async ({
  113 |   page,
  114 | }) => {
  115 |   await page.emulateMedia({ reducedMotion: "reduce", colorScheme: "dark" });
  116 |   await page.setViewportSize({ width: 390, height: 844 });
  117 |   await page.reload();
  118 | 
  119 |   const overflow = await page.evaluate(
  120 |     () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
  121 |   );
  122 |   expect(overflow).toBeLessThanOrEqual(1);
  123 | 
  124 |   const transitionDuration = await page
  125 |     .getByRole("button", { name: "Copy value" })
  126 |     .first()
  127 |     .evaluate((element) => getComputedStyle(element).transitionDuration);
  128 |   const longestTransitionSeconds = Math.max(
  129 |     ...transitionDuration
  130 |       .split(",")
  131 |       .map((duration) => Number.parseFloat(duration.trim())),
  132 |   );
  133 |   expect(longestTransitionSeconds).toBeLessThanOrEqual(0.001);
  134 | });
  135 | 
  136 | test("matches the reviewed desktop viewport baseline", async ({ page }) => {
  137 |   await page.setViewportSize({ width: 1440, height: 1000 });
  138 |   await page.reload();
  139 |   await page.evaluate(() => document.fonts.ready);
> 140 |   await expect(page).toHaveScreenshot("brand-kit-page.png", {
      |                      ^ Error: expect(page).toHaveScreenshot(expected) failed
  141 |     animations: "disabled",
  142 |     fullPage: false,
  143 |   });
  144 | });
  145 | 
```