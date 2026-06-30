# Sample Prompts

Start the local server by running `uv run adk web` and select **`src`** in the top-left dropdown (if not already selected). 

You can try these prompts to test all workflow branches, routing rules, and constraints:

---

## 1. Happy Path — Verified Vehicle (Full Reservation Flow)
#### Prompt:
```text
I'm employee E007, my plate is KA07NP5678, and I want to park for 1 hour starting now.
```
#### Expected Behavior:
1. The **`vehicle_verification_agent`** successfully verifies vehicle `V007` (an SUV owned by Suresh Kumar, employee `E007`).
2. The verification router outputs `"PROCEED"`.
3. Parallel execution splits:
   - **`slot_finder_agent`** searches for available SUV spots and recommends a slot ID (e.g., `S007` / `1-SUV-007`).
   - **`charge_calculator_agent`** calculates the hourly rate for SUV (`45.00 INR` for 1 hour).
4. The system joins the branches and displays a clean **Reservation Summary**.
5. The server pauses execution (`RequestInput`), asking: *"Would you like to confirm this reservation? Reply Yes to confirm or No to cancel."*

#### Confirmation:
```text
Yes
```
#### Expected Behavior:
The database record is inserted, the slot availability is set to `0`, and a confirmation message with the Reservation ID is returned.

---

## 2. Constraint Path — Already Reserved Vehicle (Early Terminate)
#### Prompt:
*Try running the exact same happy path prompt a second time (or query another vehicle with an active booking):*
```text
I'm employee E007, my plate is KA07NP5678, and I want to park for 1 hour starting now.
```
#### Expected Behavior:
The system checks the database, finds that vehicle `V007` already has an active confirmed booking, outputs:
> *"Your vehicle already has an active reservation! You cannot book another slot."*

and **halts execution immediately** (parallel slot matching and pricing steps are skipped).

---

## 3. Constraint Path — Unregistered Vehicle (Early Terminate)
#### Prompt:
```text
I'm employee E004, my plate is KA99ZZ9999, and I want to book a spot for 2 hours.
```
#### Expected Behavior:
The system determines the vehicle is not in the database and outputs:
> *"Your vehicle is not registered. Please register your vehicle first!"*

and **halts execution immediately** (parallel slot matching and pricing steps are skipped).

---

## 4. Slot Availability Filter (Specific Floor Lookup)
#### Prompt:
```text
I'm employee E003, my plate is KA03EF9012, and I want a slot for 1.5 hours. I prefer floor 1.
```
#### Expected Behavior:
- Vehicle is verified (SUV owned by Priya Nair).
- Slot search filters specifically for floor `1`.
- Pricing bills for a rounded duration of `1.5 hours` (billed in 30-minute increments).

---

## 5. EV Discount Tier Lookup
#### Prompt:
```text
I'm employee E008, my plate is KA08QR9012, and I want to reserve a slot for 3 hours.
```
#### Expected Behavior:
- Vehicle `V008` is verified as an **EV** (Tata MG ZS EV owned by Meera Patel).
- Hourly charge rate calculation applies the EV discounted rate tier (`25 INR` per hour).
