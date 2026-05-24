#include "pap.h"

bool pap::predict_branch(champsim::address ip)
{
  auto idx = hash(ip);
  auto value = pht[idx][bht[idx]];
  return value.value() > (value.maximum / 2);
}

void pap::last_branch_result(champsim::address ip, champsim::address branch_target, bool taken, uint8_t branch_type)
{
  auto idx = hash(ip);
  pht[idx][bht[idx]] += taken ? 1 : -1;

  bht[idx] = ((bht[idx] << 1) | (taken ? 1 : 0)) & ((1 << LHR_BITS) - 1);
}