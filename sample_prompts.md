# Sample Prompts & Commands

### 🖥️ 1. Test Locally (Development Server)
To run the developer server locally:
```bash
uv run adk web
```

### ☁️ 2. Test Deployed Cloud Agent
To connect the developer Web UI to your live cloud agent deployed on Vertex AI Reasoning Engine:
```bash
uv run adk web src --session_service_uri "agentengine://projects/project-8f12ea6a-1eb5-4330-a3b/locations/us-central1/reasoningEngines/4364778038026567680"
```

You can use the following prompts to test all branches and constraints in the Web UI:

---

## 1. Happy Path — Verified Vehicle (Full Reservation Flow)

**Step A - Initial Request:**
```text
I'm employee E007, my plate is KA07NP5678, and I want to park for 1 hour starting now.
```

**Step B - Confirmation Prompt:**
```text
Yes
```

---

## 2. Constraint Path — Already Reserved Vehicle (Early Terminate)

*Try running the exact same happy path prompt a second time:*
```text
I'm employee E007, my plate is KA07NP5678, and I want to park for 1 hour starting now.
```

---

## 3. Constraint Path — Unregistered Vehicle (Early Terminate)

```text
I'm employee E004, my plate is KA99ZZ9999, and I want to book a spot for 2 hours.
```

---

## 4. Slot Availability Filter (Specific Floor Lookup)

```text
I'm employee E003, my plate is KA03EF9012, and I want a slot for 1.5 hours. I prefer floor 1.
```

---

## 5. EV Discount Tier Lookup

```text
I'm employee E008, my plate is KA08QR9012, and I want to reserve a slot for 3 hours.
```
