package iluminara

allow if {
  input.region == "FR"
  input.framework == "FR_CNIL"
  input.data_type != "personal_data"
}
