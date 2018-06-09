
update eva_verb 
set (PROCESS_DESC_REF_ID) = (@PDR.$PROCESS_DESC_REF_ID)
where ENTITY_DEF_ID = @ED.$ENTITY_DEF_ID and name ='$VERB_NAME';

