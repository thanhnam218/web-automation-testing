# AUTOMATION TEST AND CI/CD PIPELINE REPORT

**Project:** Fashion Store Web Automation Testing  
**Pipeline Manager:** GitHub Actions  
**Tech Stack:** Java (Spring Boot), MySQL, JUnit 5, Python (Selenium Webdriver), PyTest  

---

## 1. PROJECT OBJECTIVES
The primary objective of this testing architecture is to ensure continuous stability across both the Back-end logic and the UI layer of the E-commerce website. By integrating a Continuous Integration/Continuous Deployment (CI/CD) pipeline via GitHub Actions, we automatically detect regressions, significantly reduce manual testing efforts, and improve overall software integrity with every pushed commit.

---

## 2. TESTING SCOPE
The automation framework is divided into two major independent test layers executed in parallel to optimize server run time:

### 2.1. Backend Unit Testing (Isolated Mock)
- **Tools:** Java 17, Maven, JUnit 5, Mockito.
- **Strategy:** Utilizing `Mocking` techniques to entirely isolate the Service layer from the physical database dependencies. This accelerates test execution and strictly validates core Business Logic.
- **Sample Test Case:** `CategoryServiceTest`
  - *Scenario 1:* Asserts proper `MessageException` handling when providing invalid inputs (e.g., duplicate IDs). Validates structural intactness of exception `getMessage()` versus custom constructors.
  - *Scenario 2:* Simulates the `CategoryRepository` retrieval process using Mockito `thenReturn()` stubs to assert successful entity persistence without real MySQL side effects.

### 2.2. Web End-to-End (E2E) UI Testing
- **Tools:** Python 3.10, PyTest, Selenium WebDriver (Headless Chrome).
- **Strategy:** Deploying fully automated browser agents to directly interact with the website's DOM precisely as a human user would.
- **Sample Test Case:** `test_homepage_loads_successfully`
  - *Scenario:* Bootstraps the real Spring Boot Context internally on the Linux Runner -> Runs a polling loop expecting HTTP 200 at port `8080` -> Instantiates headless WebDriver to visit the URL.
  - *Pass Criteria:* DOM loads successfully, the HTML Document captures the expected website Title without throwing `ERR_CONNECTION_REFUSED`.

---

## 3. CI/CD PIPELINE ARCHITECTURE
To maintain an active 24/7 validation infrastructure, the GitHub Actions architecture orchestrates two YAML workflows:

1. **Virtual Database Provisioning:** Automatically spins up a MySQL 8.0 Service Container inside the GitHub Runner, mapping port `3306` to seamlessly match `application.properties`.
2. **Security & Secrets Management:** Configured GitHub Actions Secrets to dynamically inject the Firebase configuration payload into `firebase-service-account.json`. This ensures the Spring Context loads fully for tests without exposing API keys publicly.
3. **Distribution & Background Deployment:** 
   - Dynamically calls the globally installed `mvn test` wrapper replacement.
   - Bootstraps the Web app via `mvn spring-boot:run &` as a background process. Implements HTTP polling mechanisms prior to executing the Python PyTest scripts to avoid synchronization timeouts.

---

## 4. TEST RESULTS & TROUBLESHOOTING LOG
The pipeline currently holds a 100% Pass rate after proactively resolving system/environment constraints.

**Isolated and Resolved Environmental Bugs:**
- 🐛 *Java NullPointerException during Test Assertion:* Fixed by redirecting `MessageException` custom internal getter, resolving JUnit assertion mismatch gracefully.
- 🐛 *Spring Boot Bean Conflict:* Identified and purged residual test components (`ProjectSellApplication.java`) sharing `@SpringBootApplication` context causing ambiguity.
- 🐛 *Firebase Auth Constraint:* Implemented automated GitHub Secret payload injection rather than bypassing logic configuration, preserving the web application's deployment readiness.
- 🐛 *Selenium Linux OS Environment Crash:* Eradicated outdated 3rd-party `webdriver-manager` parsing bugs (caused by headless ZIP package restructuring) by upgrading native Selenium Driver Management support (v4.6.0+).

**CONCLUSION:** Total Pipeline Green Rate: **100%**. 
The Automation framework perfectly supports future feature branches and is fully resilient against environment teardowns.
