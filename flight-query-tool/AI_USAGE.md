# AI Usage Disclosure

## Tools Used

- OpenAI ChatGPT — GPT-6, used for programming guidance, explanations, debugging and selected code assistance.
- GitHub Codespaces — used as the development environment for implementing and testing the application.

## Conversation Links

- Link 1: https://chatgpt.com/share/6b0061ef-732c-83ed-b01d-4768fb854da1
- Link 2: https://chatgpt.com/share/6b00666b-2820-83eb-b65c-d5a6fb231d12

## How AI Assistance Was Used

AI assistance was used selectively throughout the development process. It helped me understand the assignment requirements, learn Python concepts, implement selected functions and troubleshoot errors. I also performed project setup, code integration, execution, testing and verification independently.

## Code Contributions and AI Assistance

| File | Part of the code | My contribution and AI assistance |
|---|---|---|
| validator.py | load_airports() | Used AI guidance to understand file reading and airport-code loading. |
| validator.py | validate_row() | Used AI assistance to understand validation rules and implement validation logic. Reviewed the validation sequence and test results. |
| validator.py | to_record() | Used AI guidance for converting validated CSV fields into the required dictionary structure. |
| csv_loader.py | parse_files() | Used AI assistance for CSV processing and duplicate detection. Integrated the function and checked its behaviour using the supplied tests. |
| flight_parser.py | main() | Used AI assistance for parts of the command-line implementation, JSON processing and logging. Integrated and tested the complete application workflow. |
| query.py | run_query(), run_queries() | Used AI assistance to understand and implement query filtering, sorting, ordering and limits. |

## Work I Performed Independently

- Set up and organised the assignment inside my existing GitHub repository.
- Created the flight-query-tool project directory and integrated the professor's starter files.
- Entered my student identification details into the application.
- Configured and used GitHub Codespaces for development.
- Studied the assignment requirements and reviewed the required function signatures.
- Executed the public test suite using Python 3.
- Analysed test output and checked the results for each grading group.
- Verified that all 29 public tests passed.
- Checked the project structure and preserved the professor's original test and sample data files.
- Prepared the AI usage disclosure and project documentation.
- Organised the implementation into separate Git commits.
- Pushed the completed development milestones to my GitHub repository.
- Reviewed the implementation and test results before preparing the submission.

## Key Prompts Used

1. Explain the assignment requirements and the architecture of the Flight Schedule Parser and Query Tool.
2. Explain Python functions, type hints, lists, dictionaries, sets and exception handling used in the project.
3. Help implement and understand flight record validation, including airport codes, date and time validation and price checks.
4. Explain CSV processing, physical line numbers, blank lines, comments and duplicate detection.
5. Explain command-line arguments, JSON file handling, error logging and program exit codes.
6. Explain query filtering, sorting, ordering and result limits.
7. Review the implementation and identify potential edge cases using the public test results.

## Testing and Verification

I executed the professor's public test suite after integrating the implementation.

Final public test result:

- Structure: 6/6
- Row validation: 3/3
- CSV parsing: 7/7
- CLI and folders: 3/3
- Duplicate detection: 2/2
- Basic queries: 4/4
- Extended queries: 2/2
- Response file: 2/2

Total: 29/29 public tests passed.

I used AI as a programming and learning assistant, while personally managing the project setup, integration, execution, testing, verification and GitHub submission.