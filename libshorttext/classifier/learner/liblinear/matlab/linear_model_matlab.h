#include <stdint.h>
#ifndef INT64_DEFINED
typedef int64_t INT64;
#define INT64_DEFINED
#endif
const char *model_to_matlab_structure(mxArray *plhs[], struct model *model_);
const char *matlab_matrix_to_model(struct model *model_, const mxArray *matlab_struct);
