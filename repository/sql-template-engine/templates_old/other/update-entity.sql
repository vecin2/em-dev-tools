update EVA_ENTITY_DEFINITION
set (LOGICAL_OBJ_PATH) = ('$LOGICAL_OBJ_PATH')
where id = @ED.Defect;

update EVA_ENTITY_DEFINITION
set (INTERFACE_PATH) = ('$INTERFACE_PATH')
where id = @ED.Defect;

update EVA_ENTITY_DEFINITION
set (NAME) = ('${ENTITY_NAME}')
where id = @ED.Defect;

