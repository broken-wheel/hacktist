At: "bad-loop-04.hac":8:
parse error: syntax error
parser stacks:
state	value
#STATE#	(null) 
#STATE#	list<(root_item)>: (instance-decl) ... [6:1--7:8]
#STATE#	( [8:1]
#STATE#	; [8:2]
#STATE#	identifier: i [8:3]
#STATE#	: [8:4]
#STATE#	(range) [8:6..17]
#STATE#	; [8:18]
in state #STATE#, possible rules are:
	loop_instantiation: '(' ';' ID ':' range . ':' instance_management_list ')'  (#RULE#)
acceptable tokens are: 
	':' (shift)
