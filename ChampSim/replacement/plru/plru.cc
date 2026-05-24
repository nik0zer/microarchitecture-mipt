#include "plru.h"
#include <cmath>
#include <cassert>

plru::plru(CACHE* cache) : plru(cache, cache->NUM_SET, cache->NUM_WAY) {}

plru::plru(CACHE* cache, long sets, long ways) : replacement(cache), NUM_WAY(ways), tree(sets, 0) {
  LOG2_WAY = std::log2(NUM_WAY);
  assert((1 << LOG2_WAY) == NUM_WAY && "PLRU requires NUM_WAY to be a power of 2");
}

long plru::find_victim(uint32_t triggering_cpu, uint64_t instr_id, long set, const champsim::cache_block* current_set, champsim::address ip,
                       champsim::address full_addr, access_type type)
{
  uint64_t curr_tree = tree[set];
  long curr_node = 0;
  long way = 0;

  for (long level = 0; level < LOG2_WAY; ++level) {
    int dir = (curr_tree >> curr_node) & 1;
    way = (way << 1) | dir;
    curr_node = curr_node * 2 + 1 + dir;
  }
  return way;
}

void plru::update_plru(long set, long way)
{
  long curr_node = 0;
  for (long level = 0; level < LOG2_WAY; ++level) {
    int dir = (way >> (LOG2_WAY - 1 - level)) & 1;
    uint64_t mask = 1ULL << curr_node;
    if (dir == 0) {
      tree[set] |= mask;
    } else {
      tree[set] &= ~mask;
    }
    curr_node = curr_node * 2 + 1 + dir;
  }
}

void plru::replacement_cache_fill(uint32_t triggering_cpu, long set, long way, champsim::address full_addr, champsim::address ip, champsim::address victim_addr,
                                  access_type type)
{
  update_plru(set, way);
}

void plru::update_replacement_state(uint32_t triggering_cpu, long set, long way, champsim::address full_addr, champsim::address ip,
                                    champsim::address victim_addr, access_type type, uint8_t hit)
{
  if (hit && access_type{type} != access_type::WRITE) {
    update_plru(set, way);
  }
}