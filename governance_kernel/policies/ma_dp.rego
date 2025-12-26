package iluminara

allow if {
  input.region == "MA"
  input.framework == "MA_DP"
  input.data_type != "personal_data"
}
