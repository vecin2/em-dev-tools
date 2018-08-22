
INSERT INTO EVA_PROCESS_DESCRIPTOR (ID, ENV_ID, NAME, REPOSITORY_PATH, CONFIG_PROCESS_ID, IS_DELETED, TYPE) 
VALUES (@PD.gscCustomerSearch, --ID
	@ENV.Dflt, --ENV_ID,
	'gscCustomerSearch', --process_descriptor_name
	'GSCCoreEntities.Implementation.Customer.Verbs.Search', --repository_path 
	NULL , --config_id
	'N',
	2 --type
);
