#ifndef BRANCH_PAP_H
#define BRANCH_PAP_H

#include <array>
#include "address.h"
#include "modules.h"
#include "msl/fwcounter.h"

class pap : champsim::modules::branch_predictor
{
  static constexpr std::size_t LHR_BITS = 6;
  static constexpr std::size_t NUM_ROWS = 256;
  static constexpr std::size_t PRIME = 251;
  static constexpr std::size_t BITS = 2;

  std::array<unsigned long, NUM_ROWS> bht{};
  std::array<std::array<champsim::msl::fwcounter<BITS>, (1 << LHR_BITS)>, NUM_ROWS> pht;

  [[nodiscard]] static constexpr auto hash(champsim::address ip) { return ip.to<unsigned long>() % PRIME; }

public:
  using branch_predictor::branch_predictor;

  bool predict_branch(champsim::address ip);
  void last_branch_result(champsim::address ip, champsim::address branch_target, bool taken, uint8_t branch_type);
};

#endif