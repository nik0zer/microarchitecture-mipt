#ifndef BRANCH_GAP_H
#define BRANCH_GAP_H

#include <array>
#include "address.h"
#include "modules.h"
#include "msl/fwcounter.h"

class gap : champsim::modules::branch_predictor
{
  static constexpr std::size_t GHR_BITS = 8;
  static constexpr std::size_t NUM_ROWS = 64;
  static constexpr std::size_t PRIME = 61;
  static constexpr std::size_t BITS = 2;

  unsigned long ghr = 0;
  std::array<std::array<champsim::msl::fwcounter<BITS>, (1 << GHR_BITS)>, NUM_ROWS> pht;

  [[nodiscard]] static constexpr auto hash(champsim::address ip) { return ip.to<unsigned long>() % PRIME; }

public:
  using branch_predictor::branch_predictor;

  bool predict_branch(champsim::address ip);
  void last_branch_result(champsim::address ip, champsim::address branch_target, bool taken, uint8_t branch_type);
};

#endif