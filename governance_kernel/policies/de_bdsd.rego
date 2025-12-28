package iluminara

allow if {
  input.region == "DE"
  input.framework == "DE_BDSD"
  input.data_type != "personal_data"
}
