INSERT INTO EVA_PROCESS_DESCRIPTOR (ID, ENV_ID, NAME, REPOSITORY_PATH, CONFIG_PROCESS_ID, IS_DELETED, TYPE) VALUES (@PD.$PROCESS_DESCRIPTOR_NAME, @ENV.Dflt, '$PROCESS_DESCRIPTOR_NAME', '$REPOSITORY_PATH', $CONFIG_PROCESS_ID, 'N', $TYPE);
INSERT INTO EVA_PROCESS_DESCRIPTOR_LOC (ID, ENV_ID, LOCALE, DISPLAY_NAME, DESCRIPTION) VALUES (@PD.$PROCESS_DESCRIPTOR_NAME, @ENV.Dflt, 'en-GB', '$PROCESS_DESCRIPTOR_NAME', '$PROCESS_DESCRIPTOR_DESCRIPTION');
