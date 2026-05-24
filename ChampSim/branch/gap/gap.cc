#include "gap.h"

bool gap::predict_branch(champsim::address ip)
{
  auto value = pht[hash(ip)][ghr];
  return value.value() > (value.maximum / 2);
}

void gap::last_branch_result(champsim::address ip, champsim::address branch_target, bool taken, uint8_t branch_type)
{
  pht[hash(ip)][ghr] += taken ? 1 : -1;
  ghr = ((ghr << 1) | (taken ? 1 : 0)) & ((1 << GHR_BITS) - 1);
}