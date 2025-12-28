package iluminara

allow if {
  input.region == "AR"
  input.framework == "AR_PDPA"
  input.data_type != "personal_data"
}
