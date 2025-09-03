# AI Agreement Parser
Extracts key milestones from license agreements (.docx) and outputs a structured CSV + run log.

## Why This Exists
- The team spends time manually skimming contracts for deadlines/milestones.
- I wanted a real, production-adjacent project using LLMs + Google APIs outside of class.
- Goal: faster triage and cleaner handoffs while keeping a human in the loop.

## What It Does (Current Capabilities)
- **Input:** `.docx` agreements (Word)
- **Output:** `milestones.csv` (structured rows) + `YYYY-MM-DD_HH-MM-SS_parser.log` (trace + errors)
- **Sources:** Files are fetched from Google Drive using service-account credentials
- **Engine:** Google Gemini API parses milestone data from document text
- **Delivery:** CSV and log are written locally, then uploaded back to Drive
- **Status:** In active use on UMN Tech Comm’s Shared Drive; works reliably with normal formatting

> Note: Parsing can vary with unusual document formatting. Prompt tuning reduces most issues.

## How It Works (Pipeline)
1. **Configure logger** (timestamped file + console).
2. **Load credentials** from a JSON service account to access Drive.
3. **Download target `.docx` files** to a working folder.
4. **Initialize CSV** with a header row (milestone fields).
5. **Call Gemini** with a strict parsing prompt per file.
6. **Append parsed rows** to the CSV; write warnings to the log.
7. **Upload CSV + log** to designated Drive folders.

### Example Output (Illustrative)
```csv
OTC Agreement Number,Milestone Name,Milestone Target Completion Date,Milestone Description,Milestone Set Deadline,Milestone Payment
A-2099-0001,PERFORMANCE MILESTONES,2099-06-30,"By June 30, 2099, Licensee will initiate first pilot production run of Licensed Product",True,
A-2099-0001,MILESTONE PAYMENTS,,"Upon first commercial sale of Licensed Product, Licensee shall pay $5,000 to University",False,5000.0
A-2100-0042,PERFORMANCE MILESTONES,2100-03-15,"By March 15, 2100, Licensee will submit regulatory approval documents",True,
A-2100-0042,PERFORMANCE MILESTONES,2100-10-01,"By October 1, 2100, Licensee will deliver annual progress report",True,
