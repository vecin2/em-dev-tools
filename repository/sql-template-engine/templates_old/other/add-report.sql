
INSERT INTO CR_REPORT (ID, REPORT_NAME, REPORT_TYPE, IS_AGENT_DEPENDED, ICON_PATH, RELEASE_ID, ENV_ID, MENU_ITEM_ID, MENU_ITEM_ENV_ID, REPORT_URL, IS_DELETED) VALUES (
	@RPRT.${REPORT_NAME},
	'${REPORT_NAME}',
	'R',
	'N',
	'/CoreReports/UI/Images/chart_column',
	@Release.ID,
	@ENV.Dflt,
	@MNI.${MNI_ID},
	@ENV.Dflt,
	'http://<JASPER_HOST>/jasperserver-pro/flow.html?_flowId=viewReportFlow&reportUnit=/SGroup_Reporting/Interaction_Reporting/reports/${REPORT_URL}',
	'N');

