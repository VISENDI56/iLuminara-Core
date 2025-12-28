package iluminara

allow if {
  input.region == "ET"
  input.framework == "ET_DP"
  input.data_type != "personal_data"
}
