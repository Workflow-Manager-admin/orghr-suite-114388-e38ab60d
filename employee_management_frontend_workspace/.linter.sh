#!/bin/bash
cd /home/kavia/workspace/code-generation/orghr-suite-114388-e38ab60d/employee_management_frontend_workspace/employee_management_frontend
npm run build
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
   exit 1
fi

