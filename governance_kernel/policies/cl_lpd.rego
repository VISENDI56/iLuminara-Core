package iluminara

allow if {
  input.region == "CL"
  input.framework == "CL_LPD"
  input.data_type != "personal_data"
}
