package iluminara

allow if {
  input.region == "CA"
  input.framework == "CA_PRIVACY_ACT"
  input.data_type != "private_information"
}
