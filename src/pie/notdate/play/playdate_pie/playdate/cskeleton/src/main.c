#include <stdio.h>
#include <stdlib.h>

#include "pd_api.h"

#ifdef _WINDLL
__declspec(dllexport)
#endif
int eventHandler(PlaydateAPI* pd, PDSystemEvent event, uint32_t arg){}
