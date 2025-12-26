package iluminara

allow if {
  input.region == "EU"
  input.framework == "EU_DIGITAL_SERVICES_ACT"
  input.data_type != "platform_data"
}
