# 🛒 Fashion Store - Enterprise Automation Testing Project

[![Spring Boot CI with Maven and MySQL](https://github.com/thanhnam218/web-automation-testing/actions/workflows/maven-test.yml/badge.svg)](https://github.com/thanhnam218/web-automation-testing/actions/workflows/maven-test.yml)
[![End-to-End UI Testing with Python Selenium](https://github.com/thanhnam218/web-automation-testing/actions/workflows/python-selenium.yml/badge.svg)](https://github.com/thanhnam218/web-automation-testing/actions/workflows/python-selenium.yml)

This repository contains the Backend source code for the **Fashion Store** E-Commerce platform, fully integrated with a highly professional **CI/CD Automation Testing Pipeline**.

---

## 💡 Overview
This project serves not just as a standard E-commerce showcase, but strictly to demonstrate the capability to establish and maintain robust software quality assurance platforms. 
Whenever new source code is pushed to the `main` branch, the GitHub Actions ecosystem instantly spins up MySQL databases, validates Backend Business Logic via Mocking Unit Tests, and spawns Headless browser robots (Python Selenium) to evaluate the Web UI integrity without human intervention.

## 🛠 Tech Stack
- **Web Core System:** Java 17, Spring Boot, MySQL.
- **CI/CD Automation:** GitHub Actions (Ubuntu-latest VMs, MySQL Service Container).
- **Backend Unit Testing:** JUnit 5, Mockito.
- **Web UI End-to-End Testing:** Python 3.10, Selenium WebDriver Headless, PyTest.
- **Security:** GitHub Secrets (Dynamic Injection of Firebase Credentials).

## 🗂 Automation Testing Structure
The framework is structurally divided into two prominent verification layers:

1. **Unit Test (Directory `src/test/java`)**
    - Extensively uses Mockito to isolate the Internal Service Layer from physical database reliance.
    - Example scenario: `CategoryServiceTest` mocks the `CategoryRepository` repository component assuring correct logic and error throwing mechanism seamlessly prior to real-world deployment.
2. **E2E UI Test (Directory `automation_tests`)**
    - Isolated Python/Selenium environment running parallel checks.
    - The testing methodology compiles the full Spring Boot application running virtually on localhost:8080. Once verified reachable through HTTP poll looping, the scripts launch a Headless Chrome interface asserting front-end components.

## 🚀 Deployment Instructions (For Forkers)

**The pipeline is purely automated. However, if you intend to fork this project locally:**
1. Navigate to your repository `Settings` -> `Secrets and variables` -> `Actions`.
2. Create a new Secret instance named `FIREBASE_JSON`.
3. Paste your Firebase Service Config JSON entirely into the secret payload.
4. Tweak your codebase logic and `git push`. The `.github/workflows/` automation logic will identify changes and execute validations efficiently!

---
*For more extensive details related to the architectural troubleshooting process and design configuration, please refer to the attached detailed [Report_Automation_Test.md](./Report_Automation_Test.md) file.*