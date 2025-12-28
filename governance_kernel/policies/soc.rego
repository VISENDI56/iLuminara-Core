package iluminara

allow if {
  input.framework == "SOC"
  input.data_type != "confidential_information"
}
