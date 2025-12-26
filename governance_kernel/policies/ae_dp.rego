package iluminara

allow if {
  input.region == "AE"
  input.framework == "AE_DP"
  input.data_type != "personal_data"
}
