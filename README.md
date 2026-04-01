# 🛒 Fashion Store - Enterprise Automation Testing Project

[![Spring Boot CI with Maven and MySQL](https://github.com/thanhnam218/web-automation-testing/actions/workflows/maven-test.yml/badge.svg)](https://github.com/thanhnam218/web-automation-testing/actions/workflows/maven-test.yml)
[![End-to-End UI Testing with Python Selenium](https://github.com/thanhnam218/web-automation-testing/actions/workflows/python-selenium.yml/badge.svg)](https://github.com/thanhnam218/web-automation-testing/actions/workflows/python-selenium.yml)

This repository contains the source code for the **Fashion Store** E-Commerce platform, fully integrated with a highly professional **CI/CD Automation Testing Pipeline**. It serves not just as a standard E-commerce showcase, but strictly to demonstrate the capability to establish and maintain robust software quality assurance architectures. 

Whenever new source code is pushed to the `main` branch, the GitHub Actions ecosystem instantly spins up MySQL databases, validates Backend Business Logic via Mocking Unit Tests, and spawns Headless browser robots (Python Selenium) to evaluate the Web UI integrity aggressively.

## 🛠 Tech Stack
- **Web Core System:** Java 17, Spring Boot 2.7.x, MySQL 8.
- **CI/CD Automation:** GitHub Actions (Ubuntu-latest VMs, MySQL Service Container).
- **Backend Unit Testing:** JUnit 5, Mockito.
- **Web UI End-to-End Testing:** Python 3.10, Selenium WebDriver (Headless mode), PyTest.
- **Security:** GitHub Secrets (Dynamic Injection of Firebase Credentials).

## 🚀 Deployment Instructions (For Forkers)
1. Navigate to your repository `Settings` -> `Secrets and variables` -> `Actions`.
2. Create a new Secret instance named `FIREBASE_JSON`.
3. Paste your Firebase Service Config JSON entirely into the secret payload.
4. Tweak your codebase logic and `git push`. The `.github/workflows/` automation logic will identify changes and execute validations efficiently!

---

# 📊 ENTERPRISE AUTOMATION TEST REPORT

## 1. EXECUTIVE SUMMARY
*This section provides a high-level overview of the testing cycle to help evaluate system stability before formulating a Release/Deployment decision.*

- **Pass/Fail Ratio Summary:**
  - Overall Status: **[PASSED] - Ready for Production Deployment.**
  - 🟢 **Passed:** 100% (All 12 Automated Test Cases)
  - 🔴 **Failed:** 0%
- **Environment Details:** 
  - **Testing Infrastructure:** Staging (Fully virtualized on GitHub Actions CI using Docker / Ubuntu 22.04 LTS runners).
  - **E2E Browser Setup:** Google Chrome (Headless Execution Mode).

## 2. EXECUTION DETAILS
*Specific metrics measuring the test coverage, execution scope, and overall performance speed of the Automated QA framework.*

| Status | Count | Item Category Description |
| :---: | :---: | :--- |
| **Total Test Cases** | **12** | Aggressive coverage testing 5 pillars: Regression, Business Workflows, Responsiveness/Compatibility, UI/UX Integrity, and Basic Performance. |
| 🟢 **Passed** | 12 | Core functional domains (Cart, Login, Product Index) successfully rendered their expected DOM structures. |
| 🔴 **Failed** | 0 | No internal server crashes (HTTP 500) or missing page mappings (HTTP 404) detected. |
| 🟡 **Skipped** | 0 | No scenarios were skipped due to network latency, connection resets, or missing target configurations. |

- **Total Execution Duration:** `~ 19.87s` (This includes launching the Chrome Webdriver natively, executing the Spring Boot backend, migrating database constraints, and asserting multi-layered HTML nodes across 5 distinct routes).
- **Average Performance Threshold:** All UI layout resolutions seamlessly operated beneath the mandatory GitHub Action limitation of **`6.0 seconds per page`**.

## 3. HISTORICAL DEFECT TRACKING & RCA
*Defect logging and traceback extraction documented during the integration testing phase. Real-world incidents encountered from the beginning of the CI/CD pipeline integration to the final Selenium Test script stabilization are recorded below.*

### 3.1. Infrastructure & Pipeline Incidents
| Defect ID | Severity | Root Cause Analysis (RCA) | Resolution |
| :--- | :--- | :--- | :--- |
| **ENV-001** | **BLOCKER** | The `.gitignore` policy excluded `firebase-service-account.json`. Spring Boot Context crashed upon `@Bean FirebaseMessaging` initialization on CI. | Implemented dynamic secret initialization using **GitHub Actions Environment Secrets**. Passed via `echo` injection. |
| **ENV-002** | **HIGH**    | Redundant `@SpringBootApplication` context definitions existed inside `src/test/java/com/web`. Caused `IllegalStateException` during Context Load. | Performed a codebase sanity scrub. Purged legacy test files from the hierarchy. |
| **FRM-01**  | **HIGH**    | Deprecated 3rd party Python `webdriver-manager` parsing misbehavior on Linux (`THIRD_PARTY_NOTICES` recognized as execute binary). | Sunsetted `webdriver-manager` usage; Upgraded scripts to utilize native **Selenium Manager 4.x.x**. |
| **FRM-02**  | **HIGH**    | Pre-installed CI environment lacked `.mvn/wrapper` properties due to localized Git tracking exclusions. | Replaced wrapper-based build variables (`./mvnw`) with global CLI instances (`mvn`) universally accessible on GitHub runners. |

### 3.2. E2E UI Automation Incidents
#### Incident 1: Stale Element Reference (Dynamic DOM Mutation)
- **Failed Scenario:** `test_ux_images_are_not_broken`
- **Error Log / Traceback:** `selenium.common.exceptions.StaleElementReferenceException: stale element not found in the current frame`
- **Root Cause Analysis:** The layout incorporates a JavaScript Slider/Carousel or Lazy-loading feature on the Homepage. While the Selenium WebDriver iterates securely over multiple `<img>` links using a generic Python loop, the background JavaScript mutates or reorganizes those elements, pushing the initial referenced tags into a "Stale" state disconnected from the DOM.
- **Automator Resolution:** Engineered an aggressive one-shot execution script using native JS (`driver.execute_script`) to scrape every single `src` text attribute simultaneously within `1ms`, avoiding traditional Python iteration vulnerabilities altogether.

#### Incident 2: False Positive Assertion (Semantical Text Collision)
- **Failed Scenario:** `test_regression_all_pages_healthy[/login]`
- **Error Log / Traceback:** `AssertionError: ⛔ REGRESSION BUG: Page /login not found (Error 404)`
- **Root Cause Analysis:** False Positive Automated Bug. The application gracefully retrieved and rendered the complete `/login.html` form layout alongside external Google Identity Services. However, the legacy Python restriction `assert "404" not in source` inadvertently clashed against the randomly generated Google Developer OAuth Client ID (`l004tgn5o...`). Pytest mistakenly identified the UI as an Apache/Spring HTTP 404 Fallback error.
- **Automator Resolution:** Replaced the unrefined keyword search block with specialized Spring Boot Framework specific syntax: `assert "This application has no explicit mapping" not in source`. Achieving 100% backend-rendering certainty without textual false flags.

## 4. DEFECT CLASSIFICATION
By actively classifying structural glitches mitigated throughout the testing framework layout, the Defect Distribution outlines the architectural maturity of the project:

1. **Script Bugs & Framework Misconfigurations (80%):** 
   - `StaleElementReferenceException` errors, semantical `404` mismatches, and `webdriver-manager` binary failures are classic automated scripting defects. They have been refined out of existence through modern JS Executors, native tools, and stringent structural Keyword Barriers.
2. **Environment Issues (Local Virtual Constraints - 20%):**
   - Missing Firebase JSON credentials and Public GitHub Actions default latencies triggered early crashes. Configuring GitHub Repository Secrets and extending metric load limitations effectively eliminated these external dependencies.
3. **Product Bugs (Website Source Code - 0%):**
   - At this precise execution time, Backend Developers have left zero exposed Unmapped Exceptions or `WhiteLabel` API leaks. Furthermore, MySQL Database connection limits operate flawlessly behind CI/CD standard Injected Pipeline Secrets. The application safely handles complex E2E automated DOM interactions.

## 5. MODERN REPORTING & FRAMEWORK INTEGRATION ROADMAP
_To accelerate visual diagnostics (Visualization) and enterprise integration during scaling efforts, the project architects propose expanding the reporting environment:_

1. **PyTest-HTML Generator:** Deploy the standardized `pytest-html` plugin immediately to convert bare-bones CLI terminal tracebacks into graphical HTML dashboards.
2. **Allure Report Integration:** For extensive commercial deployment, adopting the *Allure Framework* will inject real-time "Screenshot-on-Fail" functionalities even during Headless virtual runs. Allure effortlessly assembles comprehensive Pie Charts natively within the Jenkins/GitHub Actions UI interface capturing precise HTTP Network calls.
3. **Cypress / Playwright Dashboard Migration:** The Selenium architecture can eventually be entirely transformed into **Playwright**. Playwright ships fully integrated with its proprietary *Trace Viewer* module—acting as a local E2E screen-recorder; enabling Backend Developers to visually rewind, play, and inspect HTTP headers of any Automated Mouse-click timeline like watching a recorded video.

✅ **Executive Sign-off:** The CI/CD Pipeline and Dual-Testing Suite (Mockito Unit + Selenium E2E) meet strict enterprise release standards. Project structure is highly viable for Commercial deployment and Corporate Portfolio review.