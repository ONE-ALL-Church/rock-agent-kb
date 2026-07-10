# Rock Mobile Block Selector Image Audit

Generated: 2026-07-10T17:26:08+00:00

This concept resource digs through official Rock Mobile block documentation pages and their screenshots to recover selector and x-ray clues useful for styling Rock RMS mobile app blocks. It complements the broader [Rock Mobile CSS X-Ray Design Resource](css-xray-design-resource.md).

## Method

- Uses 91 official block-page source URLs under `developer/mobile-docs/essentials/blocks`.
- Uses the reviewed selector inventory in [mobile-block-selector-xray.jsonl](../mobile-block-selector-xray.jsonl).
- Selector rows preserve evidence type and confidence so OCR-derived callouts do not outrank explicit official text tables.
- Source dependency hashes are recorded in [mobile-block-selector-xray-dependencies.json](../mobile-block-selector-xray-dependencies.json).
- Private crawl/OCR scratch files may exist under `data/review/mobile-block-image-audit/`; those are review inputs, not public source artifacts.

## Findings

- Many block pages still have no styling x-ray or explicitly say no styling x-ray is available because the block renders a XAML template.
- The most useful selector data appears in x-ray screenshots for finance, reminders, communication, check-in, profile, notes, and group blocks.
- Content-style blocks usually need semantic `StyleClass` hooks in the authored XAML rather than relying on generated block internals.
- Apple Vision OCR was more reliable than Gemma for exact label/class extraction from documentation screenshots.

## Machine-Readable Inventory

The selector inventory is available as JSONL at [knowledge/concepts/mobile/mobile-block-selector-xray.jsonl](../mobile-block-selector-xray.jsonl).

## Selector Inventory

### Blocks overview

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks](https://community.rockrms.com/developer/mobile-docs/essentials/blocks)

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| setting_or_xray_context | Rock:Zone.Expands="True": outer layout property for full-height block content | image_ocr_or_page_text | reviewed |
| setting_or_xray_context | Integrated Scroll: blocks with this badge should not be wrapped by an extra scrolling layout | image_ocr_or_page_text | reviewed |

### Check-in

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/check-in/check-in](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/check-in/check-in)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `check-in-title` | Label | title text | image_xray_ocr | ocr_reviewed |
| `check-in-subtitle` | Label | subtitle text | image_xray_ocr | ocr_reviewed |
| `check-in-next-button` | Button | next/continue button | image_xray_ocr | ocr_reviewed |
| `check-in-avatar` | Avatar | person/avatar image | image_xray_ocr | ocr_reviewed |
| `check-in-person-name` | Label | person name | image_xray_ocr | ocr_reviewed |

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| note | Integrated Scroll block. Block settings override page parameters. | page_text | reviewed |

### Content

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content)

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| setting_or_xray_context | Mobile Settings: Cache Duration, Process Lava On Server, Process Lava On Client, Show On Phone, Show On Tablet, Requires Network | image_ocr_or_page_text | reviewed |
| setting_or_xray_context | Basic Settings: Content, Enabled Lava Commands, Dynamic Content, Context Entity Type | image_ocr_or_page_text | reviewed |
| setting_or_xray_context | Context Parameters: page advanced settings can provide context parameter names | image_ocr_or_page_text | reviewed |
| note | The page explicitly states there is no styling X-Ray because this block renders a XAML template. Add semantic StyleClass hooks in owned XAML. | page_text | reviewed |

### Content Collection View

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content-collection-view](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content-collection-view)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `search-field-frame` | StyledBorderView | search field frame | image_xray_ocr | ocr_reviewed |
| `menu-button` | IconButton | menu/filter button | image_xray_ocr | ocr_reviewed |
| `search-field` | SearchFieldView | search input | image_xray_ocr | ocr_reviewed |
| `no-results-container` | Grid | no-results wrapper | image_xray_ocr | ocr_reviewed |
| `no-results-icon` | Icon | no-results icon | image_xray_ocr | ocr_reviewed |
| `no-results-label` | Label | no-results title | image_xray_ocr | ocr_reviewed |
| `no-results-subtitle` | Label | no-results subtitle | image_xray_ocr | ocr_reviewed |

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| setting_or_xray_context | XAML Template: template surface for list/no-result UI | image_ocr_or_page_text | reviewed |

### Content Channel Item View

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content-channel-item-view](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/content-channel-item-view)

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| note | No selector rows recovered from images; block works like Content with a XAML template. | page_text | reviewed |

### Hero

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/hero](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/hero)

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| setting_or_xray_context | Process Lava On Server: needed when the block title/content uses Lava | image_ocr_or_page_text | reviewed |
| note | No useful selector rows recovered from images. | page_text | reviewed |

### Profile Details

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/profile-details](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/profile-details)

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| setting_or_xray_context | Mobile Local Settings: show/require field toggles follow a repeated field pattern | image_ocr_or_page_text | reviewed |
| setting_or_xray_context | Mobile Settings: device/network block settings remain relevant | image_ocr_or_page_text | reviewed |

### Structured Content View

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/structured-content-view](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/cms/structured-content-view)

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| setting_or_xray_context | Editor Tool Configuration: content channel default content control for structured content | image_ocr_or_page_text | reviewed |
| note | The page says no styling X-Ray is available. | page_text | reviewed |

### Communication Entry

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-entry](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-entry)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `entry-recipient-icon` | Icon | recipient icon | image_xray_ocr | ocr_reviewed |
| `entry-recipient-icon` | Label | recipient label area in x-ray image | image_xray_ocr | ocr_reviewed |
| `entry-chevron` | Icon | recipient row chevron | image_xray_ocr | ocr_reviewed |
| `entry-configuration-text` | Label | configuration text | image_xray_ocr | ocr_reviewed |
| `entry-configuration-parent-toggle-text` | Label | parent toggle text | image_xray_ocr | ocr_reviewed |
| `entry-email` | FieldContainer | email field | image_xray_ocr | ocr_reviewed |

### Communication List Subscribe

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-list-subscribe](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/communication-list-subscribe)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `communicationlist-item` | View | communication list item | official_text | high |
| `communicationlist-item-name` | Label | list item name | official_text | high |
| `communicationlist-item-description` | Label | list item description | official_text | high |

### SMS Conversation

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/sms-conversation](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/sms-conversation)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `sms-profile-picture` | Image | profile image | manual_image_review | high |
| `sms-full-name` | Label | conversation person full name | manual_image_review | high |
| `sms-phone-icon` | Icon | phone action icon | manual_image_review | high |
| `bubble-inbound-layout` | StackLayout | inbound bubble wrapper | manual_image_review | high |
| `bubble-inbound-text` | Label | inbound message body | manual_image_review | high |
| `bubble-inbound-date` | Label | inbound message date | manual_image_review | high |
| `sms-camera` | Icon | camera icon | manual_image_review | high |
| `sms-bolt` | Icon | snippet/shortcut icon | manual_image_review | high |
| `sms-send-icon` | Icon | send icon | manual_image_review | high |

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| note | Also exposes Rock custom CSS properties for inbound/outbound bubble background and text colors. | page_text | reviewed |

### SMS Conversation colors

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/sms-conversation](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/sms-conversation)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `-rock-inbound-background-color` | CSS custom property | inbound bubble background | official_text | high |
| `-rock-inbound-text-color` | CSS custom property | inbound text color | official_text | high |
| `-rock-outbound-background-color` | CSS custom property | outbound bubble background | official_text | high |
| `-rock-outbound-text-color` | CSS custom property | outbound text color | official_text | high |

### SMS Conversation List

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/sms-conversation-list](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/communication/sms-conversation-list)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `header-view` | Grid | list header | image_xray_ocr | ocr_reviewed |
| `expand-icon` | Icon | expand/collapse icon | image_xray_ocr | ocr_reviewed |
| `recipient-profile-image` | Image | recipient image | image_xray_ocr | ocr_reviewed |
| `sms-conversations-list-collection` | ListView | conversation collection | image_xray_ocr | ocr_reviewed |

### Connection Request Detail

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-detail)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `connection-request-detail-layout` | ScrollView | outer content wrapper | official_text | high |
| `connection-request-detail-frame` | Frame | main content wrapper | official_text | high |
| `connection-request-detail-content` | StackLayout | content within frame wrapper | official_text | high |
| `status-pill-layout` | FlexLayout | pill content wrapper | official_text | high |
| `contact-button-[xxx]` | Button | contact action button, where xxx is action name such as Mobile | official_text | high |
| `request-activities-frame` | Frame | activities section wrapper | official_text | high |
| `request-activities` | StackLayout | activity content wrapper | official_text | high |
| `add-activity-sheet` | StackLayout | CoverSheet content wrapper | official_text | high |
| `activity-container` | Grid | individual activity wrapper | official_text | high |

### Connection Request Detail image x-ray

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/connection/connection-request-detail)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `pill-request-opportunity` | Tag | opportunity pill | image_xray_ocr | ocr_reviewed |
| `pill-campus` | Tag | campus pill | image_xray_ocr | ocr_reviewed |
| `pill-critical` | Tag | critical pill | image_xray_ocr | ocr_reviewed |
| `person-name` | Label | person name | image_xray_ocr | ocr_reviewed |
| `person-connection-status` | Label | connection status | image_xray_ocr | ocr_reviewed |
| `request-details` | Grid | request details grid | image_xray_ocr | ocr_reviewed |
| `activity-person-name` | Label | activity person name | image_xray_ocr | ocr_reviewed |
| `activity-text` | Label | activity body text | image_xray_ocr | ocr_reviewed |
| `activity-list` | StackLayout | activity list | image_xray_ocr | ocr_reviewed |

### Attribute Values

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/attribute-values)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `panel-label` | Label | panel/group label | image_xray_ocr | ocr_reviewed |
| `panel-item-name` | Label | attribute name | image_xray_ocr | ocr_reviewed |
| `panel-item-value` | Label | attribute value | image_xray_ocr | ocr_reviewed |
| `panel-item-chevron` | Icon | row chevron | image_xray_ocr | ocr_reviewed |

### My Notes

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/my-notes](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/my-notes)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `my-note-filter` | IconButton | filter action | image_xray_ocr | ocr_reviewed |
| `my-notes-title` | Label | title | image_xray_ocr | ocr_reviewed |
| `my-notes-section-header` | Label | section header | image_xray_ocr | ocr_reviewed |

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| setting_or_xray_context | XAML Template: template surface for notes list UI | image_ocr_or_page_text | reviewed |

### Notes

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/notes](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/notes)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `note-item-name` | Label | note name | image_xray_ocr | ocr_reviewed |
| `note-item-text` | Label | note text | image_xray_ocr | ocr_reviewed |
| `note-item-date` | Label | note date | image_xray_ocr | ocr_reviewed |
| `note-item-avatar` | Avatar | avatar | image_xray_ocr | ocr_reviewed |
| `note-item-chevron` | Icon | row chevron | image_xray_ocr | ocr_reviewed |

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| setting_or_xray_context | Entity Type: block setting for note entity scope | image_ocr_or_page_text | reviewed |
| setting_or_xray_context | Body CSS Class: page advanced setting visible in image context | image_ocr_or_page_text | reviewed |

### Quick Note

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/quick-note](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/quick-note)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `quick-note-text-editor` | TextEditor | note editor | image_xray_ocr | ocr_reviewed |
| `quick-note-send` | StyledBorder | send action wrapper | image_xray_ocr | ocr_reviewed |

### Search

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/search](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/search)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `search-layout` | Layout | search outer layout | official_text | high |
| `search-field-layout` | Layout | search field layout | official_text | high |
| `search-frame` | Frame | search frame | official_text | high |
| `search-icon` | Icon | search icon | official_text | high |
| `search-loading-indicator` | ActivityIndicator | loading indicator | official_text | high |
| `results-layout` | Layout | results wrapper | official_text | high |
| `results-layout-inner` | Layout | inner results wrapper | official_text | high |
| `results-header` | Label | results heading | official_text | high |
| `results-collection-layout` | CollectionView | results collection | official_text | high |
| `loading-more` | ActivityIndicator | load more indicator | official_text | high |

### Smart Search

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/smart-search](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/core/smart-search)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `smart-search-icon` | Icon | search component icon | image_xray_ocr | ocr_reviewed |
| `smart-search-result-avatar` | Avatar | result avatar | image_xray_ocr | ocr_reviewed |
| `smart-search-result-name` | Label | result name | image_xray_ocr | ocr_reviewed |
| `smart-search-result-email` | Label | result email | image_xray_ocr | ocr_reviewed |
| `smart-search-result-chevron` | Icon | result chevron | image_xray_ocr | ocr_reviewed |

### Person Profile

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/person-profile](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/crm/person-profile)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `profile-action-button` | VerticalButton | profile action button | image_xray_ocr | ocr_reviewed |
| `profile-action-button-grid` | Grid | action button grid | image_xray_ocr | ocr_reviewed |
| `panel-label` | Label | panel label | image_xray_ocr | ocr_reviewed |
| `panel-item-name` | Label | panel item name | image_xray_ocr | ocr_reviewed |
| `panel-item-value` | Label | panel item value | image_xray_ocr | ocr_reviewed |
| `panel-item-chevron` | Icon | panel item chevron | image_xray_ocr | ocr_reviewed |

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| setting_or_xray_context | Body CSS Class: page advanced CSS class field visible in screenshot | image_ocr_or_page_text | reviewed |
| setting_or_xray_context | Context Parameters: page context parameter section visible in screenshot | image_ocr_or_page_text | reviewed |

### Calendar Event List

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-event-list](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-event-list)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `calendar-event` | View | event item | official_text | high |
| `calendar-event-title` | Label | event title | official_text | high |
| `calendar-event-summary` | Label | event summary | official_text | high |
| `calendar-event-text` | Label | event text | official_text | high |
| `calendar-event-audience` | Label | audience | official_text | high |
| `calendar-event-campus` | Label | campus | official_text | high |
| `next-month` | Button | next month control | official_text | high |
| `previous-month` | Button | previous month control | official_text | high |

### Calendar View

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-view](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/events/calendar-view)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `calendar-toolbar` | Layout | calendar toolbar | official_text | high |
| `calendar-toolbar-current-month` | Label | current month | official_text | high |
| `calendar-toolbar-adjacent-month` | Label | adjacent month | official_text | high |
| `calendar-day` | View | day cell | official_text | high |
| `calendar-day-title` | Label | day label | official_text | high |
| `calendar-event` | View | event item | official_text | high |
| `calendar-event-title` | Label | event title | official_text | high |
| `calendar-filter` | View | filter control | official_text | high |

### Financial Batch Detail

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-detail)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `batch-title` | Label | batch title | image_xray_ocr | ocr_reviewed |
| `batch-detail-date-title` | Label | date title | image_xray_ocr | ocr_reviewed |
| `batch-detail-title` | Label | detail title | image_xray_ocr | ocr_reviewed |
| `batch-detail-body` | Label | detail body | image_xray_ocr | ocr_reviewed |
| `batch-detail-amount-title` | Label | amount title | image_xray_ocr | ocr_reviewed |
| `batch-detail-item-title` | Label | item title | image_xray_ocr | ocr_reviewed |
| `batch-detail-container` | StyledBorderView | detail container | image_xray_ocr | ocr_reviewed |
| `batch-detail-amount-totals` | Label | amount totals | image_xray_ocr | ocr_reviewed |
| `batch-detail-currency-totals` | Label | currency totals | image_xray_ocr | ocr_reviewed |
| `batch-detail-note-title` | Label | note title | image_xray_ocr | ocr_reviewed |
| `refresh-button` | Icon | refresh action | image_xray_ocr | ocr_reviewed |
| `transaction-detail-container` | StyledBorderView | transaction container | image_xray_ocr | ocr_reviewed |
| `transaction-amount` | Label | transaction amount | image_xray_ocr | ocr_reviewed |
| `transaction-accounts` | Label | transaction accounts | image_xray_ocr | ocr_reviewed |
| `transaction-datetime` | Label | transaction date/time | image_xray_ocr | ocr_reviewed |
| `transaction-code` | Label | transaction code | image_xray_ocr | ocr_reviewed |

### Financial Batch List

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-list](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/financial-batch-list)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `batch-list-title` | Label | batch list title | image_xray_ocr | ocr_reviewed |
| `batch-list-filter` | IconButton | filter button | image_xray_ocr | ocr_reviewed |

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| setting_or_xray_context | XAML Template: template surface for batch rows | image_ocr_or_page_text | reviewed |

### Giving

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/giving](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/giving)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `campus-picker` | Picker | campus picker | image_xray_ocr | ocr_reviewed |
| `menu-button` | IconButton | menu button | image_xray_ocr | ocr_reviewed |
| `add-another-fund-icon` | Icon | add fund icon | image_xray_ocr | ocr_reviewed |
| `payment-method-frame` | Grid | payment method wrapper | image_xray_ocr | ocr_reviewed |
| `payment-method-icon` | Icon | payment method icon | image_xray_ocr | ocr_reviewed |
| `payment-method-label` | Label | payment method label | image_xray_ocr | ocr_reviewed |
| `coverage-label` | Label | coverage/fee label | image_xray_ocr | ocr_reviewed |
| `giving-option-frame` | StyledBorder | giving option wrapper | image_xray_ocr | ocr_reviewed |
| `coverage-amount` | Label | coverage amount | image_xray_ocr | ocr_reviewed |
| `giving-option-title` | Label | option title | image_xray_ocr | ocr_reviewed |
| `process-date-picker` | DatePicker | gift date picker | image_xray_ocr | ocr_reviewed |

### Transaction Detail

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/transaction-detail](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/transaction-detail)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `accounts-grid` | Grid | accounts grid | image_xray_ocr | ocr_reviewed |
| `accounts-amount` | Label | account amount | image_xray_ocr | ocr_reviewed |
| `form-field-title` | Label | form field title | image_xray_ocr | ocr_reviewed |
| `form-field` | View | form field wrapper | image_xray_ocr | ocr_reviewed |
| `account-name` | Label | account name | image_xray_ocr | ocr_reviewed |

### Transaction List

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/transaction-list](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/finance/transaction-list)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `year-picker` | Picker | year picker | image_xray_ocr | ocr_reviewed |
| `month-header` | Label | month heading | image_xray_ocr | ocr_reviewed |
| `transaction-amount` | Label | amount | image_xray_ocr | ocr_reviewed |
| `transaction-date` | Label | date | image_xray_ocr | ocr_reviewed |
| `transaction-account-list` | StackLayout | account list | image_xray_ocr | ocr_reviewed |
| `navigation-icon` | Icon | navigation icon | image_xray_ocr | ocr_reviewed |
| `transaction-account` | Label | account | image_xray_ocr | ocr_reviewed |
| `default-card` | StyledBorder | transaction card | image_xray_ocr | ocr_reviewed |

### Group Attendance Entry

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-attendance-entry)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `group-attendance-entry-layout` | Layout | outer layout | image_xray_ocr | ocr_reviewed |
| `group-attendance-datepicker` | StyledBorderView | date picker wrapper | image_xray_ocr | ocr_reviewed |
| `group-attendance-toggle` | ContentView | attendance toggle wrapper | image_xray_ocr | ocr_reviewed |
| `toggle-title` | Label | toggle title | image_xray_ocr | ocr_reviewed |
| `toggle-button` | StyledBorderView | toggle button | image_xray_ocr | ocr_reviewed |
| `group-attendance-note` | TextEditor | note editor | image_xray_ocr | ocr_reviewed |
| `save-button` | Button | save button | image_xray_ocr | ocr_reviewed |

### Group Edit

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-edit](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-edit)

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| setting_or_xray_context | Show Header: block setting visible in screenshot | image_ocr_or_page_text | reviewed |

### Group Finder

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-finder)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `campus-picker` | Picker | campus filter | official_text | high |
| `day-of-week-picker` | Picker | day filter | official_text | high |
| `time-of-day-picker` | Picker | time filter | official_text | high |
| `group-finder-filter` | IconButton | filter action | official_text | high |
| `group-finder-search-button` | Button | search action | official_text | high |

### Group Member List

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-member-list](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/group-member-list)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `member-list-title` | Label | member list title | image_xray_ocr | ocr_reviewed |
| `member-list-filter` | IconButton | filter button | image_xray_ocr | ocr_reviewed |

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| setting_or_xray_context | XAML Template: template surface for member rows | image_ocr_or_page_text | reviewed |

### Schedule Preference

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-preference](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-preference)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `assignment-field-container` | FieldContainer | assignment field | image_xray_ocr | ocr_reviewed |
| `group-schedule-title` | Label | schedule title | image_xray_ocr | ocr_reviewed |
| `group-schedule-subtitle` | Label | schedule subtitle | image_xray_ocr | ocr_reviewed |
| `assignment-title` | Label | assignment title | image_xray_ocr | ocr_reviewed |
| `assignment-detail` | Label | assignment detail | image_xray_ocr | ocr_reviewed |

### Schedule Sign Up

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-sign-up](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/groups/schedule-sign-up)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `signup-header` | Label | signup header | image_xray_ocr | ocr_reviewed |
| `group-header` | Label | group header | image_xray_ocr | ocr_reviewed |
| `toggle-title` | Label | toggle title | image_xray_ocr | ocr_reviewed |
| `toggle-append-text` | Label | toggle appended text | image_xray_ocr | ocr_reviewed |
| `toggle-button` | StyledBorderView | toggle button | image_xray_ocr | ocr_reviewed |

### Reminder Dashboard

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/reminders/reminder-dashboard](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/reminders/reminder-dashboard)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `reminder-card-count` | Label | card count | image_xray_ocr | ocr_reviewed |
| `reminder-card` | StyledBorderView | dashboard card | image_xray_ocr | ocr_reviewed |
| `reminder-card-type` | Label | card type | image_xray_ocr | ocr_reviewed |
| `reminder-types-section-title` | Label | section title | image_xray_ocr | ocr_reviewed |
| `reminder-type-count` | Label | type count | image_xray_ocr | ocr_reviewed |
| `reminder-type-title` | Label | type title | image_xray_ocr | ocr_reviewed |
| `reminder-type-subtitle` | Label | type subtitle | image_xray_ocr | ocr_reviewed |
| `reminder-type-more` | Label | more text | image_xray_ocr | ocr_reviewed |
| `reminder-card-icon` | Icon | card icon | image_xray_ocr | ocr_reviewed |

### Reminder Edit

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/reminders/reminder-edit](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/reminders/reminder-edit)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `reminder-date-picker` | DatePicker | date picker | image_xray_ocr | ocr_reviewed |
| `reminder-text-editor` | TextEditor | text editor | image_xray_ocr | ocr_reviewed |
| `reminder-picker` | Picker | generic picker | image_xray_ocr | ocr_reviewed |
| `reminder-person-picker` | PersonPicker | person picker | image_xray_ocr | ocr_reviewed |
| `reminder-duration` | NumberBox | duration | image_xray_ocr | ocr_reviewed |
| `reminder-repeat` | NumberBox | repeat interval | image_xray_ocr | ocr_reviewed |
| `reminder-save-button` | Button | save button | image_xray_ocr | ocr_reviewed |

| Context | Note | Evidence | Confidence |
| --- | --- | --- | --- |
| note | Header Template is a styling tweak surface per page text. | page_text | reviewed |

### Reminder List

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/reminders/reminder-list](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/reminders/reminder-list)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `reminder-title` | Label | title | image_xray_ocr | ocr_reviewed |
| `reminder-note` | Label | note | image_xray_ocr | ocr_reviewed |
| `reminder-date` | Label | date | image_xray_ocr | ocr_reviewed |
| `reminder-type` | Label | type | image_xray_ocr | ocr_reviewed |
| `reminder-list-avatar` | Avatar | avatar | image_xray_ocr | ocr_reviewed |
| `reminder-chevron` | Icon | chevron | image_xray_ocr | ocr_reviewed |
| `complete-icon` | Icon | complete action | image_xray_ocr | ocr_reviewed |

### Onboard Person

Source: [https://community.rockrms.com/developer/mobile-docs/essentials/blocks/security/onboard-person](https://community.rockrms.com/developer/mobile-docs/essentials/blocks/security/onboard-person)

| Selector | Element | Use | Evidence | Confidence |
| --- | --- | --- | --- | --- |
| `onboarding-title` | Label | title | image_xray_ocr | ocr_reviewed |
| `onboarding-subtitle` | Label | subtitle | image_xray_ocr | ocr_reviewed |
| `onboarding-advance-button` | Button | advance action | image_xray_ocr | ocr_reviewed |
| `onboarding-previous-button` | Button | previous action | image_xray_ocr | ocr_reviewed |

## Use Rules

- Treat `official_text` rows as strongest because they come from page text or style-class tables.
- Treat `image_xray_ocr` and `manual_image_review` rows as strong design clues, but verify against the current live docs and app shell before making production changes.
- If a block exposes a template setting, prefer adding your own semantic `StyleClass` hooks inside the template.
- If a block has no x-ray and no template, style only with documented block/page/device selectors and verify in the rendered app.
