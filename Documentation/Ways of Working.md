## <u><b>Brewed Awakening</b></u>
### <u><b>Ways of Working</b></u>

This document serves to outline our approach to Ways of Working, which is a collaborative effort that can be edited by all parties involved as needed.

### <u><b>Development Process</b></u>

- We start with a daily stand-up meeting (10 minutes) to review our current to-do/doing tickets and track progress.
- Roles are assigned to specific tickets based on their size and urgency.
- During the initial sprint, we work together on one ticket at a time. As the project scope expands over subsequent weeks, we may work more independently.
- New branches are created for epics, which require review before being merged into the main branch.
- We hold weekly retrospectives to discuss the events of the past week, highlighting what went well, what didn't go well, areas for improvement, and new features to be considered.


### <u><b>Definition of Done</b></u>

- Tickets are considered done when their acceptance criteria have been met.
- Any issues or bugs identified during testing are reviewed, addressed, and resolved.
- Functionality without testing is considered "half-done," while functionality with thorough unit testing is considered "fully done."
- Code in branches must be reviewed and approved by at least one other team member before it can be merged into the main branch.
- Products are tested from the perspective of the user, using different scenarios to ensure they are working and "user-proof."

### <u><b>Technologies Used</b></u>

- Python 3.11 with the following modules: Pandas, OS, IPython
- AWS Server 
- PostgreSQL 
- Jupyter Notebook
- Docker
- Trello Tickets
- GitHub Repositories

### <u><b>Test Driven Development</b></u>

Our preferred approach is to follow test-driven development, where thorough unit testing is done before function development to ensure robust code.

### <u><b>Team Principles</b></u>

- Respect each other and communicate respectfully.
- Be punctual and present for meetings as well as project time.
- Inform team members in advance of any planned absences or early departures.
- Do not upload any functionality to the main branch until it is approved by all team members.
- If unable to resolve a ticket, ask for help.
- Tickets should be resolved in a timely manner, otherwise it becomes the team's responsibility to complete them.
- Strive to create the best possible project.

### <u><b>Coding Standards</b></u>

- Follow the principle of KISS (Keep It Simple, Stupid!) - functions should ideally have a single responsibility.
- Use comments generously in the code to make it easier for others to understand.
- Adhere to the PEP8 Standard for handling Regular Expressions.
Use proper indentation in the code.

### <u><b>Commit Messages</b></u>

- Commit messages should be informative, expressing all the steps taken, but should not be overly long to maintain readability.
- Commit messages should be professional and related to the changes made.
- Each commit should relate to an isolated feature, rather than having multiple commit messages for the same changes.
