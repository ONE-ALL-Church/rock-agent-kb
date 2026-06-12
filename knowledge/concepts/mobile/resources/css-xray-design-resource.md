# Rock Mobile CSS X-Ray Design Resource

Date: 2026-06-03

This resource is for collecting and using "x-ray" data when styling Rock RMS mobile app pages, blocks, and XAML elements. It is intentionally practical: capture the surface, choose the least brittle selector, apply supported Downhill/XAML classes, and verify on real devices or screenshots.

## Source Summary

Primary sources checked:

- [Rock Mobile Styling](https://community.rockrms.com/developer/mobile-docs/styling): Rock Mobile CSS is useful, but XAML styling is first-class in .NET MAUI, CSS is a supporting layer, and unsupported/mistyped CSS can stop an app from loading.
- [Rock Mobile Custom CSS](https://community.rockrms.com/developer/mobile-docs/styling/legacy/custom-css): documents global app CSS, inline `StyleSheet`, page/block/platform/device selectors, control selectors, inherited-control selectors, color variables, and custom Rock properties.
- [Rock Mobile Blocks](https://community.rockrms.com/developer/mobile-docs/essentials/blocks): mobile apps use Rock pages and blocks; some blocks have integrated scroll; full-height block content should use `Rock:Zone.Expands="True"` on the outer layout.
- [Content Block](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content): the Content block renders Lava and XAML and exposes mobile-specific settings such as Dynamic Content, server/client Lava processing, cache duration, device visibility, network requirement, enabled Lava commands, and context entity type.
- [Rock Mobile Colors](https://community.rockrms.com/developer/mobile-docs/styling/style-guide/colors): documents interface colors, strong/soft semantic color pairs, CSS utility classes, `?color-*` variables, and XAML palette color usage for light/dark styling.
- [Rock Mobile Style Framework Migration](https://community.rockrms.com/developer/mobile-docs/styling/style-guide/migrating): documents the `Mobile Style Framework` setting and warns that Standard, Blended, and Legacy modes materially affect dark-mode responsiveness.
- [Rock Mobile Shell Components](https://community.rockrms.com/developer/mobile-docs/styling/style-guide/shell-components): documents shell-level status bar, navigation bar, tab bar, iOS navigation transparency, and custom shell CSS properties.
- [Style Guide Walkthrough](https://community.rockrms.com/developer/mobile-docs/styling/style-guide/walkthrough): shows modern utility classes such as `p-16`, `bg-interface-softest`, `border`, `border-interface-soft`, `rounded`, `title3`, `bold`, and `text-interface-strongest` in XAML `StyleClass` attributes.
- [Rock.DownhillCss source](https://github.com/SparkDevNetwork/Rock/tree/develop/Rock.DownhillCss): public source for generated Downhill utility classes and color/spacing defaults.
- [Rock Mobile Block Selector Image Audit](block-selector-image-audit.md): repo-local crawl of official block pages and screenshot OCR that captures block-specific selector callouts and settings-only x-ray clues.

Image review:

- Downloaded official documentation screenshots for the Custom CSS app Styles tab, Content block settings, block expansion example, and style guide example into private review storage.
- Crawled 83 official mobile block pages and ran Apple Vision OCR on 113 local image files from those pages. This recovered block-specific selector labels that are recorded separately in the [Rock Mobile Block Selector Image Audit](block-selector-image-audit.md).
- Gemma 4 12B image analysis was attempted locally, then retried with resized JPEG screenshots. Text mode worked, but image mode was not reliable enough for this resource: a tiny 320px screenshot returned malformed/inaccurate label analysis, a 640px screenshot misread important labels, and a larger settings screenshot timed out after 180 seconds. Do not treat Gemma image output as source evidence for this resource.
- Manual image review added only visible setting names and workflow cues. Selectors in this overview come from text docs and Downhill source; block-specific screenshot labels are kept in the selector image audit with evidence and confidence fields.

## X-Ray Capture Schema

Capture this for every page/block you want to style:

```yaml
surface:
  app_name:
  rock_core_version:
  mobile_shell_version:
  mobile_style_framework: Standard | Blended | Legacy | unknown
  platform_tested: [ios, android]
  device_type_tested: [phone, tablet]
  color_scheme_tested: [light, dark]
page:
  page_id:
  page_guid:
  route_or_link:
  page_name:
  page_css_class:
  zone_name:
block:
  block_id:
  block_name:
  block_type_name:
  expected_block_selector: ".block-{block type name lowercase}"
  zone_expands: true | false | unknown
  integrated_scroll: true | false | unknown
  show_on_phone: true | false | unknown
  show_on_tablet: true | false | unknown
  requires_network: true | false | unknown
  cache_duration:
content_block:
  dynamic_content: true | false | unknown
  process_lava_on_server: true | false | unknown
  process_lava_on_client: true | false | unknown
  enabled_lava_commands: []
  context_entity_type:
xaml:
  root_control:
  named_controls:
  style_classes_seen: []
  custom_css_classes_seen: []
  rock_controls_seen: []
  form_or_field_controls_seen: []
style_target:
  desired_change:
  safest_selector:
  fallback_selector:
  css_or_xaml_change:
  color_tokens_or_hardcoded_colors_seen: []
  verification_screenshots: []
```

## Selector Ladder

Use the narrowest selector that expresses the real intent.

| Target | Selector or field | Use when | Source |
| --- | --- | --- | --- |
| Platform | `.ios`, `.android` | Platform-specific differences that cannot be solved with a common style | Custom CSS |
| Device type | `.phone`, `.tablet` | Layout or type must differ by phone/tablet | Custom CSS |
| Page | `.page-{configured-page-css-class}` | One page needs a local override | Custom CSS |
| Block type | `.block-{block type name lowercase}` | You need to scope a rule to one mobile block type | Custom CSS |
| Control type | `label`, `datepicker`, `button`, `fieldstack`, etc. | You need all controls of one XAML type | Custom CSS |
| Control inheritance | `^fieldstack`, `^grid`, etc. | You need a control and descendants/inherited controls | Custom CSS |
| Explicit XAML class | `StyleClass="my-class"` then `.my-class` | You own the XAML and can add a durable hook | XAML Styling / Style Guide |

Avoid starting with highly compounded selectors like `.ios.phone.page-aboutus .block-content .heading1`. The docs show this is possible, but also warn that this is usually a sign the styling strategy is fighting the framework.

## Recommended Targeting Pattern

Prefer this order:

1. Add a semantic `StyleClass` in XAML when you own the Content block or template.
2. Scope it by page CSS class if the style is page-specific.
3. Scope it by block selector only if the same block type appears in multiple contexts and needs shared treatment.
4. Scope by platform/device only when the rendered behavior differs by platform/device.
5. Use inherited selectors such as `^fieldstack` only for broad field/control families after screenshot verification.

Example:

```xml
<Rock:StyledBorder
    StyleClass="profile-callout, p-16, bg-interface-softest, border, border-interface-soft, rounded">
    <Label
        StyleClass="profile-callout-title, title3, bold, text-interface-strongest"
        Text="{{ CurrentPerson.FullName }}" />
</Rock:StyledBorder>
```

```css
.page-profile .profile-callout {
    border-color: ?color-primary-strong;
}

.page-profile .profile-callout-title {
    color: ?color-interface-strongest;
}
```

## Downhill Utility Families

From Rock's public `Rock.DownhillCss` source:

| Family | Pattern | Notes |
| --- | --- | --- |
| Typography | `.largetitle`, `.title1`, `.title2`, `.title3`, `.headline`, `.body`, `.callout`, `.subheadline`, `.footnote`, `.caption1`, `.caption2` | Generated from named Apple-style text sizes. Class names are lowercased from the source names. |
| Font emphasis | `.bold`, `.italic` | Useful in XAML `StyleClass` lists. |
| Application/interface colors | `.bg-{color}`, `.text-{color}`, `.border-{color}` | Modern colors include interface and strong/soft accent families such as `interface-strongest`, `interface-softest`, `primary-strong`, `primary-soft`, `brand-strong`, `success-soft`, etc. |
| Palette colors | `.bg-{color}-{intensity}`, `.text-{color}-{intensity}`, `.border-{color}-{intensity}` | Palette names include gray, red, orange, yellow, green, teal, blue, indigo, purple, and pink with intensity values. |
| Spacing | `.m-*`, `.ml-*`, `.mt-*`, `.mr-*`, `.mb-*`, `.mx-*`, `.my-*`, `.p-*`, `.pl-*`, `.pt-*`, `.pr-*`, `.pb-*`, `.px-*`, `.py-*` | Mobile standard spacing values include `0`, `4`, `8`, `16`, `24`, `48`, `80`, plus legacy values. |
| Layout spacing | `.spacing-*`, `.gap-*`, `.gap-row-*`, `.gap-column-*` | Generated for Standard/Blended mobile frameworks, not Legacy-only mode. |
| Sizing | `.h-*`, `.w-*` | Uses the same spacing values. |
| Borders | `.border`, `.border-0`, `.border-1`, `.border-2`, `.border-4`, `.border-8` | `.border` applies a 1-unit border. |
| Buttons | `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-success`, `.btn-info`, `.btn-warning`, `.btn-danger`, `.btn-brand`, `.btn-default`, `.btn-link-*`, `.btn-outline-*`, `.btn-sm`, `.btn-lg` | Prefer built-in button classes before inventing custom button styles. |
| Radius/alignment | `.rounded-none`, `.rounded-sm`, `.rounded`, `.rounded-lg`, `.rounded-full`, `.text-start`, `.text-center`, `.text-end` | Radius values differ between Standard and Legacy frameworks; verify the active style framework. |

## CSS Variables And Crash Risks

Rock Mobile supports `?` variables such as:

- `?color-primary-strong`, `?color-primary-soft`, `?color-interface-strongest`, `?color-interface-softest`.
- Legacy/application variables such as `?color-primary`, `?color-secondary`, `?color-success`, `?color-danger`, `?color-warning`, `?color-light`, `?color-dark`.
- Palette variables such as `?color-orange-400`.
- Alert variables such as `?color-primary-background`, `?color-primary-border`, `?color-primary-text`.
- Misc variables such as `?radius-base`, `?spacing-base`, `?font-size-default`, `?color-background`.

Guardrail: the Custom CSS docs warn that invalid `?` variables can crash the app. Treat variables as code, not design notes. Verify spelling against the active framework/source before deploying.

## Dark Mode And Color-Scheme Workflow

The previous version of this resource only had dark mode as a final verification item. That is not enough for app design work. Treat light/dark behavior as part of the x-ray data model, because Rock Mobile styling can change depending on mobile shell version, Rock Core version, `Mobile Style Framework`, platform, and whether the surface is native XAML, shell chrome, or WebView/HTML.

Official Rock Mobile docs describe modern interface colors as the intended dark-mode-aware foundation. Interface values such as `Interface-Strongest`, `Interface-Stronger`, `Interface-Strong`, `Interface-Medium`, `Interface-Soft`, `Interface-Softer`, and `Interface-Softest` are designed around light/dark strength changes. Accent pairs such as `Primary-Strong` / `Primary-Soft`, `Success-Strong` / `Success-Soft`, `Danger-Strong` / `Danger-Soft`, and `Warning-Strong` / `Warning-Soft` are the semantic alternatives to hardcoded brand or status colors. Use those values through Downhill classes, `?color-*` variables, or `Rock:PaletteColor` references before inventing custom hex colors.

Capture these fields before changing color rules:

- Active `Mobile Style Framework`: Standard should be the default for new MAUI apps and enables full modern light/dark responsiveness; Blended can produce a mixed app where some surfaces respond to dark mode and legacy surfaces do not; Legacy preserves pre-v6 styling behavior.
- The exact color surface: native XAML control, Rock block chrome, page CSS, shell status/navigation/tab bar, WebView/HTML, image asset, icon, or markdown/HTML content.
- All hardcoded color values in the target XAML/CSS: `#fff`, `#000`, named colors like `white`, `black`, `lightgray`, and fixed brand colors.
- All semantic color tokens/classes already present: `bg-interface-softest`, `text-interface-strongest`, `border-interface-soft`, `bg-primary-soft`, `text-primary-strong`, `?color-interface-softest`, `?color-interface-stronger`, and `Rock:PaletteColor`.
- Light and dark screenshots for iOS and Android when the page is user-facing or shell-adjacent.

Prefer this native XAML pattern:

```xml
<Rock:StyledBorder
    StyleClass="profile-callout, p-16, bg-interface-softest, border, border-interface-soft, rounded">
    <Label
        StyleClass="profile-callout-title, title3, bold, text-interface-strongest"
        Text="{{ CurrentPerson.FullName }}" />
</Rock:StyledBorder>
```

Prefer this CSS pattern when custom CSS is required:

```css
.page-profile .profile-callout {
    background-color: ?color-interface-softest;
    border-color: ?color-interface-soft;
}

.page-profile .profile-callout-title {
    color: ?color-interface-strongest;
}
```

Avoid this unless the value has been deliberately tested in both schemes:

```css
.page-profile .profile-callout {
    background-color: #ffffff;
    color: #000000;
}
```

Dark-mode review checklist:

- Verify the active app is not still in Legacy mode unless that is intentional.
- Verify Blended mode does not leave legacy block CSS with light-only colors on top of modern responsive surfaces.
- Verify text, icons, borders, dividers, placeholder text, disabled text, and secondary labels separately; a card can pass while its placeholder or helper text fails.
- Verify field-heavy controls: `Picker`, `DatePicker`, `TextBox`, `TextEditor`, `FieldContainer`, `FieldStack`, campus/person pickers, and validation messages.
- Verify shell chrome: status bar foreground, navigation bar background/text, tab bar selected/unselected colors, iOS navigation separator, and iOS transparent/blurred navigation bars.
- Verify Rock content controls that commonly combine background and text: `Tag`, `Button`, `StyledBorder`, `NotificationBox`, cards, modals/cover sheets, markdown/HTML, and WebView.
- Verify image and logo assets on dark backgrounds. Prefer transparent/tintable assets or explicit light/dark variants for assets with embedded text.
- Verify platform differences. iOS dark mode has had control-specific fixes in mobile release notes, including a v4.0 BibleBrowser picker white-on-white issue.
- Verify live theme switching only after deploy/reload behavior is understood. If a setting or style framework change requires deploy, do not judge dark-mode behavior from an old bundle.

Selector guidance for dark mode:

- Add explicit semantic `StyleClass` hooks for custom callouts and blocks, then keep color values semantic.
- Scope fixes to `.page-*` or `.block-*` when only one surface is wrong. Avoid global `label`, `button`, or `^grid` color overrides unless the whole app is being rethemed.
- Use `.ios` / `.android` only after screenshots prove a platform-specific native control issue.
- Treat WebView/HTML as a separate color system. Native Rock `?color-*` CSS variables do not automatically guarantee an embedded web page has a correct `prefers-color-scheme` implementation.
- Keep screenshot evidence with the x-ray record. A source-backed selector plus a dark screenshot is the minimum proof for a promoted public KB claim.

## Where To Put Styles

Use global app CSS for reusable style tokens and utility classes:

- Application Detail.
- Styles tab.
- Advanced Options.
- CSS Styles editor.

Use inline page CSS only for a page-specific experiment or a tightly scoped Content block:

```xml
<Grid>
    <Grid.Resources>
        <StyleSheet>
            <![CDATA[
            ^grid {
                background-color: lightgray;
            }
            ]]>
        </StyleSheet>
    </Grid.Resources>
</Grid>
```

## Content Block X-Ray Notes

For Content blocks, capture the configuration before styling:

- `Dynamic Content`: if `No`, content changes generally need deploy; if `Yes`, content refreshes on initialization.
- `Process Lava On Server`: needed for server-side Lava work and current-person/entity context patterns.
- `Process Lava On Client`: capture separately; do not assume server and client processing are equivalent.
- `Enabled Lava Commands`: style work can break behavior if the XAML relies on entity, SQL, workflow, web request, or other Lava commands.
- `Context Entity Type`: affects what the block renders and which records are available.
- `Cache Duration`, `Show On Phone`, `Show On Tablet`, `Requires Network`: explain platform-specific render differences before blaming CSS.

## Full-Height And Scroll Rules

For full-height content:

```xml
<Grid RowDefinitions="*"
      Rock:Zone.Expands="True">
    ...
</Grid>
```

Use `Rock:Zone.Expands="True"` on the outermost layout when a block should stretch to the full zone/screen. Do not wrap integrated-scroll blocks in another scrolling layout unless the block documentation says that combination is safe.

## Practical X-Ray Workflow

1. Capture the page/block/app fields in the schema above.
2. Copy the exact XAML around the visual problem.
3. List all existing `StyleClass` values and control names.
4. Identify whether the desired change belongs to XAML structure, a Downhill utility, or custom CSS.
5. Add a semantic class if the XAML is under your control.
6. Use the selector ladder to scope the rule.
7. Test on iOS and Android, phone and tablet where relevant.
8. Keep screenshot evidence before/after.
9. If a screenshot suggests a target but no source/XAML confirms it, treat it as a visual symptom, not a selector.

## Gemma / Image Use

Use image understanding as a reviewer helper only:

- Good use: summarize what a screenshot shows, identify visible setting labels, flag clipping/spacing/contrast problems, compare before/after renders.
- Bad use: invent selectors or class names from pixels.
- Current local result: Gemma 4 12B image mode should not be used as an authority for Rock Mobile docs screenshots until accuracy and latency improve. Manual review or a dedicated OCR/vision pass is still required for screenshot labels.
- Promotion rule: only source-backed selector claims should enter public KB guidance. Screenshot/Gemma notes can support QA, but selectors must come from XAML, Rock docs, Downhill source, or live x-ray data.

## External Sources Checked

Search found no better third-party canonical source for Rock Mobile CSS targeting than Rock's own docs and the public `Rock.DownhillCss` source. General .NET MAUI CSS documentation is useful for supported-property behavior, but Rock-specific selectors, Downhill classes, and block/page scoping come from Rock documentation.
