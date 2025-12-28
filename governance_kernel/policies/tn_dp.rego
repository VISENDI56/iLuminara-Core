package iluminara

allow if {
  input.region == "TN"
  input.framework == "TN_DP"
  input.data_type != "personal_data"
}
