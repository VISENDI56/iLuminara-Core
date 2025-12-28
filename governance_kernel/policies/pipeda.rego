package iluminara

allow if {
  input.region == "CA"
  input.framework == "PIPEDA"
  input.data_type != "personal_information"
}
