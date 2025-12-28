package iluminara

allow if {
  input.region == "KE"
  input.framework == "KE_DP"
  input.data_type != "personal_data"
}
