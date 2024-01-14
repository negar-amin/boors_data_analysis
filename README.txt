1.Please first run poetry install.
2.If you want to run each program seperately you can run them by giving them their special arguments:
first module{name: extract_transactions_xlsx_files, arguments: start_date, end_date}

second module{name: convert_xlsx_files_to_csv_files, arguments: [-c CLEAR_XLSX_FILES] stage_directory}
WARNING: here stage_directory is the directory we want to create stage folder in it if you attach stage to end of stage_directory program will create another stage folder in it!

third module{name: analyze_transactions, arguments: stage_directory}
WARNING: here stage_directory is the exact directory of stage folder created by second module.

main module{name: main, arguments: start_date, end_date, stage_directory}
USAGE: if you want to run all previous three modules in correct order you can run this module.
enter stage_directory in the way as same as stage_directory in second module.
