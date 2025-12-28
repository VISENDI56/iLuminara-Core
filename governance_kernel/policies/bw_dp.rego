package iluminara

allow if {
  input.region == "BW"
  input.framework == "BW_DP"
  input.data_type != "personal_data"
}
