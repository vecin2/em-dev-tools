INSERT INTO EVA_ENTITY__ENTITLEMENT (ENTITLEMENT_ID, ENTITLEMENT_ENV_ID, ENTITY_ID, ENTITY_ENV_ID, ENTITY_TYPE_ID, ENTITY_TYPE_ENV_ID, IS_DELETED, RELEASEID) VALUES (@ENTLMNT.${ENTITLEMENT_ID}, @ENV.Dflt, ${ENTITY_ID}, @ENV.Dflt, @ET.${ENTITY_TYPE_ID}, @ENV.Dflt, 'N', @RELEASE.ID);

