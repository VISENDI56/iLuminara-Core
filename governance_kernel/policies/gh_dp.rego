package iluminara

allow if {
  input.region == "GH"
  input.framework == "GH_DP"
  input.data_type != "personal_data"
}
