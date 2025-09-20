# MilestoneMiner

A portfolio project demonstrating advanced document parsing and automation using LLMs and Google APIs. This tool extracts key milestones from license agreements (.docx) and outputs structured CSV files alongside detailed run logs.

## Features
- Parses `.docx` license agreements to identify and extract milestone data.
- Generates structured `milestones.csv` files for easy review and analysis.
- Creates timestamped logs for traceability and error tracking.
- Integrates with Google Drive via service account credentials for seamless file management.
- Employs Google Gemini API to accurately parse milestone information from document text.
- Supports local and organizational modes for flexible deployment.

## Modes
- **MODE=local**: Runs the parser using local directories for input and output files. Ideal for personal use or testing without Drive integration.
- **MODE=org**: Connects directly to an organization's Google Drive using service account credentials, automating file download and upload processes within shared drives.

## Setup & Security
1. Create a `.env` file to store sensitive configuration variables (e.g., API keys, service account paths, mode selection).
2. Never commit `.env` files or Google service account JSON credentials to version control.
3. Use environment variables to securely manage access credentials.
4. If keys or credentials are ever exposed, rotate them immediately to maintain security.
5. Keep dependencies flexible to allow easy updates and integration with your environment.

## Example Output
```csv
OTC Agreement Number,Milestone Name,Milestone Target Completion Date,Milestone Description,Milestone Set Deadline,Milestone Payment
A-2099-0001,PERFORMANCE MILESTONES,2099-06-30,"By June 30, 2099, Licensee will initiate first pilot production run of Licensed Product",True,
A-2099-0001,MILESTONE PAYMENTS,,"Upon first commercial sale of Licensed Product, Licensee shall pay $5,000 to University",False,5000.0
A-2100-0042,PERFORMANCE MILESTONES,2100-03-15,"By March 15, 2100, Licensee will submit regulatory approval documents",True,
A-2100-0042,PERFORMANCE MILESTONES,2100-10-01,"By October 1, 2100, Licensee will deliver annual progress report",True,
```

## Roadmap
- Enhance parsing robustness with improved prompt tuning and error handling.
- Develop an interactive user interface for easier file selection, configuration, and real-time result visualization.
- Expand support for additional document formats and contract types.
- Integrate notification systems to alert users of upcoming milestones automatically.
- Optimize for scalability to handle large batches of agreements efficiently.

This project showcases practical application of AI and cloud APIs for contract management automation, emphasizing security best practices and real-world usability.
