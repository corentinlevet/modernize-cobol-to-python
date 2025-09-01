# Test Plan — Account Management System (COBOL)

This test plan captures the existing business logic of the COBOL application (`main.cob`, `operations.cob`, `data.cob`) so stakeholders can validate current behavior before/while porting to Python.

Use this plan to run interactive scenarios against the COBOL app and record the Actual Result and Status (Pass/Fail).

## Quick checklist

- Includes columns: Test Case ID, Description, Pre-conditions, Test Steps, Expected Result, Actual Result, Status, Comments — Done
- Covers business logic from `main.cob`, `operations.cob`, and `data.cob` (menu, read/write storage, credit, debit, insufficient funds, edge cases) — Done
- Leaves Actual Result and Status blank for stakeholder validation — Done

## Test Plan

| Test Case ID | Test Case Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status (Pass/Fail) | Comments |
|---|---|---:|---|---|---|---|---|
| TC-01 | Menu: valid choices 1-4 route to correct actions | App started, initial balance 1000.00 | 1) At menu enter `1` → observe. 2) Return to menu, enter `2` → observe prompt for credit. 3) Return, enter `3` → observe prompt for debit. 4) Return, enter `4`. | 1) Displays current balance. 2) Shows "Enter credit amount:" prompt. 3) Shows "Enter debit amount:" prompt. 4) Program exits with "Exiting the program. Goodbye!" |  |  | Validate each menu mapping matches current behavior |
| TC-02 | View balance (TOTAL) displays stored balance | App started, `STORAGE-BALANCE` = 1000.00 | At menu enter `1` | Displays "Current balance: 1000.00" (matching storage format) |  |  | Confirms `DataProgram READ` returns storage value |
| TC-03 | Credit a valid positive amount and persist | Start balance 1000.00 | 1) Choose `2`. 2) Enter `200.50`. 3) After success, choose `1` to view balance. | After credit, displays "Amount credited. New balance: 1200.50". Viewing balance shows 1200.50 (persistence across calls) |  |  | Confirms add + write flow and persistence |
| TC-04 | Debit a valid amount less than balance | Start balance 1000.00 | 1) Choose `3`. 2) Enter `250.25`. 3) Choose `1` to view | Displays "Amount debited. New balance: 749.75". Viewing balance shows 749.75 |  |  | Confirms subtract + write flow |
| TC-05 | Debit an amount equal to the balance → zero balance | Start balance 500.00 (setup) | 1) Choose `3`. 2) Enter `500.00`. 3) Choose `1` | Displays "Amount debited. New balance: 0.00". Viewing shows 0.00 |  |  | Edge: exact-equality allowed |
| TC-06 | Debit amount greater than balance → insufficient funds, no change | Start balance 300.00 | 1) Choose `3`. 2) Enter `400.00`. 3) Choose `1` | Displays "Insufficient funds for this debit." Balance remains 300.00 |  |  | Confirms guard prevents negative balances in normal debit case |
| TC-07 | Multiple sequential operations persist correctly | Start balance 1000.00 | 1) Choose `2`, credit `100.00`. 2) Choose `3`, debit `50.00`. 3) Choose `1` | After credit: 1100.00; after debit: 1050.00; view shows 1050.00 |  |  | Confirms cumulative operations and storage updates |
| TC-08 | Credit zero amount | Start balance 1000.00 | 1) Choose `2`. 2) Enter `0.00`. 3) Choose `1` | Displays "Amount credited. New balance: 1000.00". Balance unchanged |  |  | Current behavior: zero allowed |
| TC-09 | Debit zero amount | Start balance 1000.00 | 1) Choose `3`. 2) Enter `0.00`. 3) Choose `1` | Displays "Amount debited. New balance: 1000.00". Balance unchanged |  |  | Current behavior: zero allowed |
| TC-10 | Credit negative amount (business rule verification) | Start balance 1000.00 | 1) Choose `2`. 2) Enter `-100.00`. 3) Choose `1` | Current implementation: accepts negative and results in balance 900.00 (i.e., reduces balance). Record actual. |  |  | This is a potential business policy gap — confirm if negative credits should be rejected |
| TC-11 | Debit negative amount (business rule verification) | Start balance 1000.00 | 1) Choose `3`. 2) Enter `-50.00`. 3) Choose `1` | Current implementation: treats negative as subtracting negative → increases balance to 1050.00. Record actual. |  |  | Potentially unintended: confirm whether negative debits are allowed |
| TC-12 | Non-numeric amount input handling | Start balance 1000.00 | 1) Choose `2` or `3`. 2) Enter `abc` (or alphanumeric) when prompted | Observe behavior: either input rejected, treated as 0.00, or causes an error. Record actual behavior and program stability. |  |  | COBOL `ACCEPT` into numeric fields has platform-dependent effects — capture exact behavior |
| TC-13 | Amount exceeding field max (overflow) | Start balance 1000.00 | 1) Choose `2`. 2) Enter `1000000.00` (1,000,000.00) which is > PIC 9(6)V99 max 999999.99 | Observe whether app rejects, truncates, raises error, or wraps. Record behaviour. |  |  | Important to know numeric limits for porting and validation |
| TC-14 | Invalid menu choice loops with message | App started | At menu enter `5` or a letter | Displays "Invalid choice, please select 1-4." and returns to menu |  |  | Verify user guidance and loop behavior |
| TC-15 | Exit option terminates program cleanly | App started | At menu enter `4` | Program shows "Exiting the program. Goodbye!" and stops |  |  | Confirms exit flag sets `CONTINUE-FLAG = 'NO'` |
| TC-16 | Data persistence across application restart | Start app, credit 100.00, exit, restart app | 1) Start app (initial). 2) Choose `2`, credit `100.00`. 3) Choose `4` to exit. 4) Restart program and choose `1`. | Expected: Current implementation resets `STORAGE-BALANCE` to initial 1000.00 on process restart (no durable persistence). Record actual to confirm. |  |  | Confirms whether storage is in-memory only (likely) — important for integration testing and DB design |
| TC-17 | READ then immediate WRITE without change | Start balance 1000.00 | 1) Choose `1` to read (TOTAL). 2) Immediately perform `2` and enter `0.00` to write same balance. 3) Choose `1` | Confirm no rounding/precision change and balance equals original (1000.00) |  |  | Verify precision and format consistency between READ/WRITE |
| TC-18 | Input and display precision test | Start balance 1000.00 | 1) Choose `2`. 2) Enter `0.1` (one decimal). 3) Choose `1` | Expected: shows 1000.10 (two-decimal behavior). Record exact displayed formatting. |  |  | Ensure decimal rounding rules are acceptable for stakeholders |


## Notes for stakeholders

- The COBOL application holds `STORAGE-BALANCE` in memory with initial value `1000.00` (see `data.cob`). It does not perform durable persistence across process restarts.
- The current implementation does not explicitly validate negative or non-numeric inputs before arithmetic; behavior may be platform-dependent. Please confirm the intended business rules for:
  - Accepting/rejecting negative amounts for credit/debit
  - Handling non-numeric input
  - Required numeric bounds and persistence guarantees

