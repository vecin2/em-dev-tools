#!/bin/bash
#read -e -p 


. ./sql/sql-base.sh
. ./sql/template-value-builder.sh
. ./svn-rev-number.sh

if [ $# -eq 1 ]; then
	REVISION=$(svn_rev_number)
elif [ $# -eq 2 ]; then
	REVISION=$2
else
	echo Usage:
	echo " module: (e.g SGroupContactHistory/sqlScripts/oracle/updates/SG0_3/IncreaseDisplaySpaceContactReasons2)"
	echo " (optional) revision: (eg. 857)"
	exit 1
fi

MODULE=$1

echo "Welcome! Current rev number is $REVISION"

echo "The sql will be generated in  $MODULE/tableData.sql"

show_menu(){
	printf '\n'
	echo " What would you like to do?
	x.  Exit
	pd. Process Descriptor
	ee. Extend Entity
	ape. Add Persistable Entity 
	ace. Add Child Entity 
	ue. Update Entity 
	av. Add verb
	rv. Rewire verb
	avp. Add verb to process desc refernce
	am. Add monitor
	rm. Remove monitor
	ar. Add Report
	ae. Add Entitlement
	me. Map Entitlement
	aq. Add queue
	ade. Add Data dictionary entry
	ms. Modify Schema
	cs. Custom Script"
	read -p "Please enter option number: " OPTION
	printf '\n'
}
modify_schema(){
	read_value TABLE_NAME TABLE_NAME
	parse_template create-table.sql
}
add_process_desc_reference(){
	read_value PROCESS_DESC_REF_ID PROCESS_DESC_REF_ID
	read_value PROCESS_DESCRIPTOR_ID PROCESS_DESCRIPTOR_ID $PROCESS_DESC_REF_ID
	parse_template add-process-desc-reference.sql
}
add_process_descriptor(){
	read_value PROCESS_DESCRIPTOR_NAME PROCESS_DESCRIPTOR_NAME
	read_value DESCRIPTION PROCESS_DESCRIPTOR_DESCRIPTION 
	read_value "REPOSITORY PATH" REPOSITORY_PATH
	read_value "CONFIG PROCESS ID" CONFIG_PROCESS_ID NULL
	read_value "type id (0=regular process, 2=action, 3=sla) - default is 0:" TYPE
	parse_template add-process-descriptor.sql
}
add_standard_verb_path(){
	set_value CONFIG_PROCESS_ID NULL
	set_value TYPE 0
	add_process_descriptor

	set_value PROCESS_DESC_REF_ID $PROCESS_DESCRIPTOR_NAME
	set_value PROCESS_DESCRIPTOR_ID $PROCESS_DESCRIPTOR_NAME
	add_process_desc_reference

	set_value PROCESS_DESC_REF_ID $PROCESS_DESC_REF_ID
}
add_verb(){
	add_standard_verb_path
	add_verb_to_pdr
}
rewire_verb(){
	printf "Enter values for new verb:\n"
	add_standard_verb_path
	read_value ENTITY_DEF_ID ENTITY_DEF_ID
	read_value VERB_NAME VERB_NAME
	parse_template rewire-verb.sql
}
add_verb_to_pdr(){
	read_value VERB_ID VERB_ID $PROCESS_DESCRIPTOR_NAME
	read_value VERB_NAME VERB_NAME
	read_value ENTITY_DEF_ID ENTITY_DEF_ID
	read_value PROCESS_DESC_REF_ID PROCESS_DESC_REF_ID
	read_value "IS_INSTANCE (Y/N)" IS_INSTANCE
	read_value IS_USER_VISIBLE IS_USER_VISIBLE
	read_value RECORD_FOR_WRAPUP RECORD_FOR_WRAPUP
	read_value "IS_LAUNCHABLE_TASK" IS_LAUNCHABLE_TASK "N"
	parse_template add-verb.sql
}
extend_entity(){
	set_value SUPER_ENTITY_DEFINITION NULL
	read_value "Entity name you would like to extend(e.g CustomerED)" ENTITY_NAME_TO_EXTEND
	read_value "Interface path you would like to override (e.g. CoreEntities.API.Interfaces.EICustomer)" INTERFACE_PATH
	read_value "Logical object path you would like to override(e.g CoreEntities.Implementation.Customer.Customer)" LOGICAL_OBJ_PATH
	read_value "New entity id (@ED. will prefix to your entry)" ENTITY_ID
	read_value "New Interface path (e.g. SPENCustomer.API.EISPENCustomer)" EXT_INTERFACE_PATH
	read_value "New logical object path (e.g SPENCustomer.Implementation.Customer.Objects.SpenCustomer)" EXT_LOGICAL_OBJ_PATH
	set_value ENTITY_NAME "Base$ENTITY_NAME_TO_EXTEND"
	parse_template extend-entity.sql
}
add_persistable_entity(){
	set_value SUPER_ENTITY_DEFINITION PersistableEntity
	add_child_entity
}
add_child_entity(){
	read_value ENTITY_ID ENTITY_ID
	read_value LOGICAL_OBJ_PATH LOGICAL_OBJ_PATH
	read_value INTERFACE_PATH INTERFACE_PATH
	read_value SUPER_ENTITY_DEFINITION SUPER_ENTITY_DEFINITION
	parse_template add-entity-definition.sql
}
update_entity(){
	read_value LOGICAL_OBJ_PATH LOGICAL_OBJ_PATH
	read_value INTERFACE_PATH INTERFACE_PATH
	read_value ENTITY_NAME ENTITY_NAME
	read_value ENTITY_ID ENTITY_ID
	parse_template update-entity.sql
}
add_monitor(){
	read_value MONITOR_ID MONITOR_ID
	read_value MONITOR_REPO_PATH MONITOR_REPO_PATH
	read_value START_REPO_PATH START_REPO_PATH
	read_value "SEQUENCE_NO from EVA_DYNAMIC_VERB_LIST" SEQUENCE_NO
	parse_template add-monitor.sql
}
remove_monitor(){
	read_value "Monitor repo path(e.g Common.Implementation.Monitor)" REPOSITORY_PATH	
	read_value DYNAMIC_VERB_ID_LIST DYNAMIC_VERB_ID_LIST
	parse_template remove-monitor.sql
}
add_report(){
	read_value "Report Name(ID)" REPORT_NAME
	read_value "MENU_ID (default OpPerformanceReports)" MNI_ID OpPerformanceReports
	read_value "Report url from (...SGroup_Reporting/Interaction_Reporting/reports)"  REPORT_URL
	parse_template add-report.sql
	prompt_enter_value "Enter locations (e.g. en-GB,fi-FI)" "LOCALE"
	IFS=',' read -r -a LOCALES <<< "$LOCALE"
	for LOCALE_ITEM in "${LOCALES[@]}" 
	do
		prompt_enter_value "$LOCALE_ITEM-DISPLAY_NAME" LOC_DISPLAY_NAME
		prompt_enter_value "$LOCALE_ITEM-LOC_DESCRIPTION" LOC_DESCRIPTION $LOC_DISPLAY_NAME
		parse_template add-report-locale.sql
	done
	#add location

}
add_entitlement(){
	read_value "ID" ENT_ID
	read_value "Display Name" ENT_DISP_NAME 
	read_value "System Name" ENT_SYSTEM_NAME
	parse_template add-entitlement.sql
}

generate(){
	read -p "Please enter a comment for this script:" COMMENT
	SQL_COMMENT="--$COMMENT"
	#Invokes methods which inside will call parse_template which sets the variable LAST_PARSED_TEMPLATE
	"$1"
  CURRENT_SQL=$LAST_PARSED_TEMPLATE
	empty_parse_buffer
 	printf "Generating SQL:\n $CURRENT_SQL"; 
	SQL=$SQL$SQL_COMMENT$'\n'$CURRENT_SQL$SEPARATOR; 
	PLACE_HOLDERS=()
}
map_entitlement(){
	prompt_enter_value "ENTITLEMENT_ID (e.g. ChatReports)" ENTITLEMENT_ID
	prompt_enter_value "ENTITY_ID (e.g @PROFILE.SUPERVISOR)" ENTITY_ID
	prompt_enter_value "ENTIY_TYPE_ID (e.g ProfileType)" ENTITY_TYPE_ID
	parse_template map-entitlement.sql	
}
add_queue(){
	prompt_enter_value "Queue name" QUEUE_NAME
	prompt_enter_value "Display queue name" QUEUE_DISPLAY_NAME
	parse_template add-queue.sql
}
add_data_entry(){
	prompt_enter_value "Full path (e.g SpenCaseED.caseData.form.location.displayName)" DATA_ENTRY_PATH 
	prompt_enter_value "Display Name(e.g Form Location)" FIELD_DISPLAY_NAME 
	set_value PARENT_ENTRY_ID null
	set_value IS_FIELD "N"
	set_value IS_RULES_RELEVANT "N"
	set_value ENTRY_DISPLAY_NAME "null"
	set_value ENTRY_TYPE "null"
	set_value "N"
	local non_fields=${DATA_ENTRY_PATH%.*}
	local arr=(${non_fields//\./ }); 
	local field=${DATA_ENTRY_PATH##*.}; 
	for i in ${arr[@]}; do 
		set_value ENTRY_NAME "$i"
		set_value DATA_ENTRY_ID "@EDD.$ENTRY_NAME"
		parse_template add-data-dictionary-entry.sql
		set_value PARENT_ENTRY_ID $DATA_ENTRY_ID
	done
	set_value IS_FIELD "Y"
	set_value IS_RULES_RELEVANT "Y"
	set_value ENTRY_TYPE "'StringField'"
	set_value ENTRY_NAME "$field"
	set_value DATA_ENTRY_ID "@EDD.$ENTRY_NAME"
	set_value ENTRY_DISPLAY_NAME "$FIELD_DISPLAY_NAME"
	parse_template add-data-dictionary-entry.sql
}
#main
PLACE_HOLDERS=()
show_menu
SEPARATOR=$'\n\n\n'
while  [ "$OPTION" != "x" ];do 
	case $OPTION in
		x   )  return ;;
		ms  ) generate modify_schema ; FILE_NAME=createTables.sql ; break ;; 
		cs  ) break ;; 
		pd  ) generate add_process_descriptor ;;
		ee  ) generate extend_entity ;;
		ape ) generate add_persistable_entity ;;
		ace ) generate add_child_entity ;;
		ue  ) generate update_entity ;;
		av  ) generate add_verb ;;
		rv  ) generate rewire_verb ;;
		avp ) generate add_verb_to_pdr ;;
		am  ) generate add_monitor ;;
		ar  ) generate add_report ;;
		ae  ) generate add_entitlement ;;
		me  ) generate map_entitlement ;;
		aq  ) generate add_queue ;;
		ade  ) generate add_data_entry ;;
		rm  ) generate remove_monitor ;;
		*   ) echo Option $OPTION is not valid. Please enter a valid option ;;
       	esac
	show_menu
done


echo $SQL
create_sql_module $MODULE $REVISION "$SQL" $FILE_NAME
