#!/bin/bash
cd /home/kavia/workspace/code-generation/orghr-suite-114388-e38ab60d/employee_management_backend_workspace/employee_management_backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

