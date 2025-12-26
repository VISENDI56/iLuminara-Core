package iluminara

allow if {
  input.region == "MW"
  input.framework == "MW_DP"
  input.data_type != "personal_data"
}
