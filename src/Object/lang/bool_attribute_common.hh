/**
	\file "Object/lang/PRS_attribute_common.hh"
	Contains base classes for all tool-independent implementations
	of bool (node) attribute classes.  
	$Id: bool_attribute_common.hh,v 1.5 2010/08/24 22:52:04 fang Exp $
 */

#ifndef	__HAC_OBJECT_LANG_BOOL_ATTRIBIBUTE_COMMON_H__
#define	__HAC_OBJECT_LANG_BOOL_ATTRIBIBUTE_COMMON_H__

#include "Object/lang/PRS_fwd.hh"
#include "util/boolean_types.hh"

namespace HAC {
namespace entity {

/**
	Parent namespace of tool-independent classes.  
	These base classes are not registered.  
 */
namespace bool_attributes {
using util::good_bool;
//=============================================================================
/**
	Convenience macro for repetitive definitions.  
	Consider using type tags to name these base classes?
	Contains an argument-checking member function.  
 */
#define	DECLARE_BOOL_ATTRIBIBUTE_COMMON_STRUCT(class_name)		\
struct class_name {							\
	typedef	bool_attribute_values_type		values_type;	\
	static								\
	good_bool							\
	__check_vals(const char*, const values_type&);			\
};	// end struct class_name


//=============================================================================
DECLARE_BOOL_ATTRIBIBUTE_COMMON_STRUCT(AllowInterference)
DECLARE_BOOL_ATTRIBIBUTE_COMMON_STRUCT(AllowWeakInterference)

//=============================================================================
/**
	Treat node as if it never switches for charge-sharing analysis.
	Useful for node that are used as static configurations.  
 */
DECLARE_BOOL_ATTRIBIBUTE_COMMON_STRUCT(PseudoStatic)

/**
	Declares that this node is driven combinationally, even if the 
	rules look dynamic, for instance.  
 */
DECLARE_BOOL_ATTRIBIBUTE_COMMON_STRUCT(IsComb)

/**
	Whether or not a keeper should be automatically generated by
	back-end tools on a dynamically driven node.  
 */
DECLARE_BOOL_ATTRIBIBUTE_COMMON_STRUCT(AutoKeeper)

//=============================================================================
// miscellaneous attributes requested by others
// TODO: make attributes plug-in extendable

DECLARE_BOOL_ATTRIBIBUTE_COMMON_STRUCT(Supply)	// is like Vdd or GND
DECLARE_BOOL_ATTRIBIBUTE_COMMON_STRUCT(Reset)	// is a reset signal

DECLARE_BOOL_ATTRIBIBUTE_COMMON_STRUCT(IsRVC1)
DECLARE_BOOL_ATTRIBIBUTE_COMMON_STRUCT(IsRVC2)
DECLARE_BOOL_ATTRIBIBUTE_COMMON_STRUCT(IsRVC3)

//=============================================================================
// subclass of bools for atomic run-time expressions
DECLARE_BOOL_ATTRIBIBUTE_COMMON_STRUCT(Atomic)

//=============================================================================
}	// end namespace attributes
}	// end namespace entity
}	// end namespace HAC

#endif	// __HAC_OBJECT_LANG_BOOL_ATTRIBIBUTE_COMMON_H__

