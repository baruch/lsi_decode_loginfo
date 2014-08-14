#!/usr/bin/env python

import sys

def decode_lsi_loginfo_numbers(val):
    """While this is the official breakdown it's not quite that normal for some codes"""
    t = (val >> 28) & 0xF
    origin = (val >> 24) & 0xF
    code = (val >> 16) & 0xFF
    spec = val & 0xFFFF
    return (t, origin, code, spec)

iop_invalid_page = ["Sub Code", 0x0000FFFF, {
0x00000000: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE", None, ""),
0x00000100: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE_RT", None, "Route Table Entry not found"),
0x00000200: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE_PN", None, "Invalid Page Number"),
0x00000300: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE_FORM", None, "Invalid FORM"),
0x00000400: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE_PT", None, "Invalid Page Type"),
0x00000500: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE_DNM", None, "Device Not Mapped"),
0x00000600: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE_PERSIST", None, "Persistent Page not found"),
0x00000700: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE_DEFAULT", None, "Default Page not found"),
0x0000E000: ("IOP_LOGINFO_CODE_FWUPLOAD_NO_FLASH_AVAILABLE", None, "Tried to upload from flash, but there is none"),
0x0000E001: ("IOP_LOGINFO_CODE_FWUPLOAD_UNKNOWN_IMAGE_TYPE", None, "ImageType field contents were invalid"),
0x0000E002: ("IOP_LOGINFO_CODE_FWUPLOAD_WRONG_IMAGE_SIZE", None, "ImageSize field in TCSGE was bad/offset in MfgPg 4 was wrong"),
0x0000E003: ("IOP_LOGINFO_CODE_FWUPLOAD_ENTIRE_FLASH_UPLOAD_FAILED", None, "Error occured while attempting to upload the entire flash"),
0x0000E003: ("IOP_LOGINFO_CODE_FWUPLOAD_ENTIRE_FLASH_UPLOAD_FAILED", None, "Error occurred while attempting to upload the entire flash"),
0x0000E004: ("IOP_LOGINFO_CODE_FWUPLOAD_REGION_UPLOAD_FAILED", None, "Error occured while attempting to upload single flash region"),
0x0000E004: ("IOP_LOGINFO_CODE_FWUPLOAD_REGION_UPLOAD_FAILED", None, "Error occurred while attempting to upload single flash region"),
0x0000E005: ("IOP_LOGINFO_CODE_FWUPLOAD_DMA_FAILURE", None, "Problem occured while DMAing FW to host memory"),
0x0000E005: ("IOP_LOGINFO_CODE_FWUPLOAD_DMA_FAILURE", None, "Problem occurred while DMAing FW to host memory"),
}]

iop_encl_mgmt = ["Sub Code", 0x0000FFFF, {
0x00060001: ("IOP_LOGINFO_CODE_ENCL_MGMT_READ_ACTION_ERR0R", None, "Read Action not supported for SEP msg"),
0x00060002: ("IOP_LOGINFO_CODE_ENCL_MGMT_INVALID_BUS_ID_ERR0R", None, "Invalid Bus/ID in SEP msg"),
}]

iop_target = ["Sub Code", 0x0000FFFF, {
0x00070001: ("IOP_LOGINFO_CODE_TARGET_ASSIST_TERMINATED", None, ""),
0x00070002: ("IOP_LOGINFO_CODE_TARGET_STATUS_SEND_TERMINATED", None, ""),
0x00070003: ("IOP_LOGINFO_CODE_TARGET_MODE_ABORT_ALL_IO", None, ""),
0x00070004: ("IOP_LOGINFO_CODE_TARGET_MODE_ABORT_EXACT_IO", None, ""),
0x00070005: ("IOP_LOGINFO_CODE_TARGET_MODE_ABORT_EXACT_IO_REQ", None, ""),
}]

iop_code = ["Code", 0x00FFFFFF, {
0x00010000: ("IOP_LOGINFO_CODE_INVALID_SAS_ADDRESS", None, ""),
0x00020000: ("IOP_LOGINFO_CODE_UNUSED2", None, ""),
0x00030000: ("IOP_LOGINFO_CODE_CONFIG_INVALID_PAGE", iop_invalid_page, ""),
0x00040000: ("IOP_LOGINFO_CODE_DIAG_MSG_ERROR", None, "Error handling diag msg - or'd with diag status"), # TODO: find diag msg codes
0x00050000: ("IOP_LOGINFO_CODE_TASK_TERMINATED", None, "Associated with Task Abort"),
0x00060000: ("IOP_LOGINFO_CODE_ENCL_MGMT", iop_encl_mgmt, ""),
0x00070000: ("IOP_LOGINFO_CODE_TARGET", iop_target, ""),
0x00080000: ("IOP_LOGINFO_CODE_LOG_TIMESTAMP_EVENT", None, ""),
}]

ir_code = ["Code", 0x00FFFFFF, {
0x00010000: ("IR_LOGINFO_RAID_ACTION_ERROR", None, ""),
0x00010001: ("IR_LOGINFO_VOLUME_CREATE_INVALID_LENGTH", None, ""),
0x00010002: ("IR_LOGINFO_VOLUME_CREATE_DUPLICATE", None, ""),
0x00010003: ("IR_LOGINFO_VOLUME_CREATE_NO_SLOTS", None, ""),
0x00010004: ("IR_LOGINFO_VOLUME_CREATE_DMA_ERROR", None, ""),
0x00010005: ("IR_LOGINFO_VOLUME_CREATE_INVALID_VOLUME_TYPE", None, ""),
0x00010006: ("IR_LOGINFO_VOLUME_MFG_PAGE4_ERROR", None, ""),
0x00010007: ("IR_LOGINFO_VOLUME_INTERNAL_CONFIG_STRUCTURE_ERROR", None, ""),
0x00010010: ("IR_LOGINFO_VOLUME_ACTIVATING_AN_ACTIVE_VOLUME", None, ""),
0x00010011: ("IR_LOGINFO_VOLUME_ACTIVATING_INVALID_VOLUME_TYPE", None, ""),
0x00010012: ("IR_LOGINFO_VOLUME_ACTIVATING_TOO_MANY_VOLUMES", None, ""),
0x00010013: ("IR_LOGINFO_VOLUME_ACTIVATING_VOLUME_ID_IN_USE", None, ""),
0x00010014: ("IR_LOGINFO_VOLUME_ACTIVATE_VOLUME_FAILED", None, ""),
0x00010015: ("IR_LOGINFO_VOLUME_ACTIVATING_IMPORT_VOLUME_FAILED", None, ""),
0x00010016: ("IR_LOGINFO_VOLUME_ACTIVATING_TOO_MANY_PHYS_DISKS", None, ""),
0x00010020: ("IR_LOGINFO_PHYSDISK_CREATE_TOO_MANY_DISKS", None, ""),
0x00010021: ("IR_LOGINFO_PHYSDISK_CREATE_INVALID_LENGTH", None, ""),
0x00010022: ("IR_LOGINFO_PHYSDISK_CREATE_DMA_ERROR", None, ""),
0x00010023: ("IR_LOGINFO_PHYSDISK_CREATE_BUS_TID_INVALID", None, ""),
0x00010024: ("IR_LOGINFO_PHYSDISK_CREATE_CONFIG_PAGE_ERROR", None, ""),
0x00010030: ("IR_LOGINFO_COMPAT_ERROR_RAID_DISABLED", None, ""),
0x00010031: ("IR_LOGINFO_COMPAT_ERROR_INQUIRY_FAILED", None, ""),
0x00010032: ("IR_LOGINFO_COMPAT_ERROR_NOT_DIRECT_ACCESS", None, ""),
0x00010033: ("IR_LOGINFO_COMPAT_ERROR_REMOVABLE_FOUND", None, ""),
0x00010034: ("IR_LOGINFO_COMPAT_ERROR_NEED_SCSI_2_OR_HIGHER", None, ""),
0x00010035: ("IR_LOGINFO_COMPAT_ERROR_SATA_48BIT_LBA_NOT_SUPPORTED", None, ""),
0x00010036: ("IR_LOGINFO_COMPAT_ERROR_DEVICE_NOT_512_BYTE_BLOCK", None, ""),
0x00010037: ("IR_LOGINFO_COMPAT_ERROR_VOLUME_TYPE_CHECK_FAILED", None, ""),
0x00010038: ("IR_LOGINFO_COMPAT_ERROR_UNSUPPORTED_VOLUME_TYPE", None, ""),
0x00010039: ("IR_LOGINFO_COMPAT_ERROR_DISK_TOO_SMALL", None, ""),
0x0001003A: ("IR_LOGINFO_COMPAT_ERROR_PHYS_DISK_NOT_FOUND", None, ""),
0x0001003B: ("IR_LOGINFO_COMPAT_ERROR_MEMBERSHIP_COUNT", None, ""),
0x0001003C: ("IR_LOGINFO_COMPAT_ERROR_NON_64K_STRIPE_SIZE", None, ""),
0x0001003D: ("IR_LOGINFO_COMPAT_ERROR_IME_VOL_NOT_CURRENTLY_SUPPORTED", None, ""),
0x00010050: ("IR_LOGINFO_DEV_FW_UPDATE_ERR_DFU_IN_PROGRESS", None, ""),
0x00010051: ("IR_LOGINFO_DEV_FW_UPDATE_ERR_DEVICE_IN_INVALID_STATE", None, ""),
0x00010052: ("IR_LOGINFO_DEV_FW_UPDATE_ERR_INVALID_TIMEOUT", None, ""),
0x00010053: ("IR_LOGINFO_DEV_FW_UPDATE_ERR_NO_TIMERS", None, ""),
0x00010054: ("IR_LOGINFO_DEV_FW_UPDATE_ERR_READING_CFG_PAGE", None, ""),
0x00010055: ("IR_LOGINFO_DEV_FW_UPDATE_ERR_PORT_IO_TIMEOUTS_REQUIRED", None, ""),
0x00010056: ("IR_LOGINFO_DEV_FW_UPDATE_ERR_ALLOC_CFG_PAGE", None, ""),
0x00020000: ("IR_LOGINFO_CODE_UNUSED2", None, ""),
}]

pl_open_fail_sub= ["SubSub Code", 0x000000FF, {
0x00000001: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_NO_DEST_TIMEOUT", None, ""),
0x00000002: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_SATA_NEG_RATE_2HI", None, ""),
0x00000003: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_RATE_NOT_SUPPORTED", None, ""),
0x00000004: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_BREAK", None, ""),
0x00000005: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_RES_INITIALIZE0", None, ""),
0x00000006: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_RES_INITIALIZE1", None, ""),
0x00000007: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_RES_STOP0", None, ""),
0x00000008: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_RES_STOP1", None, ""),
0x00000009: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_RETRY", None, ""),
0x0000000A: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_BREAK", None, ""),
0x0000000B: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_UNUSED_0B", None, ""),
0x0000000C: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_OPEN_TIMEOUT_EXP", None, ""),
0x0000000D: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_UNUSED_0D", None, ""),
0x0000000E: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_DVTBLE_ACCSS_FAIL", None, ""),
0x00000011: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_BAD_DEST", None, ""),
0x00000012: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_RATE_NOT_SUPP", None, ""),
0x00000013: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_PROT_NOT_SUPP", None, ""),
0x00000014: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_ABANDON0", None, "Open Reject (Zone Violation) - available on SAS-2 devices"),
0x00000015: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_ABANDON1", None, ""),
0x00000016: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_ABANDON2", None, ""),
0x00000017: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_ABANDON3", None, ""),
0x00010018: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_STP_RESOURCES_BSY", None, ""),
0x00010019: ("PL_LOGINFO_SUB_CODE_OPEN_FAIL_WRONG_DESTINATION", None, ""),
0x0000001A: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_ORR_TIMEOUT", None, "Open Reject (Retry) Timeout"),
0x0000001B: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_PATH_BLOCKED", None, ""),
0x0000001C: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE_AWT_MAXED", None, "Arbitration Wait Timer Maxed"),
0x00000020: ("PL_LOGINFO_SUB_CODE_TARGET_BUS_RESET", None, ""),
0x00000030: ("PL_LOGINFO_SUB_CODE_TRANSPORT_LAYER", None, "Leave lower nibble (1-f) reserved."),
0x00000040: ("PL_LOGINFO_SUB_CODE_PORT_LAYER", None, "Leave lower nibble (1-f) reserved."),
}]

pl_open_fail_discovery = ["SubSub Code", 0x000000FF, {
0x00000000: ("PL_LOGINFO_SUB_CODE_DISCOVERY_SATA_INIT_W_IOS", None, ""),
0x00000001: ("PL_LOGINFO_SUB_CODE_DISCOVERY_REMOTE_SEP_RESET", None, ""),
}]

pl_open_fail = ["Sub Code", 0x0000FF00, {
0x00000100: ("PL_LOGINFO_SUB_CODE_OPEN_FAILURE", pl_open_fail_sub, ""),
0x00000200: ("PL_LOGINFO_SUB_CODE_INVALID_SGL", None, ""),
0x00000300: ("PL_LOGINFO_SUB_CODE_WRONG_REL_OFF_OR_FRAME_LENGTH", None, ""),
0x00000400: ("PL_LOGINFO_SUB_CODE_FRAME_XFER_ERROR", None, ""),
0x00000400: ("PL_LOGINFO_SUB_CODE_FRAME_XFER_ERROR", None, "Bits 0-3 encode Transport Status Register (offset 0x08)"),
0x00000500: ("PL_LOGINFO_SUB_CODE_TX_FM_CONNECTED_LOW", None, ""),
0x00000600: ("PL_LOGINFO_SUB_CODE_SATA_NON_NCQ_RW_ERR_BIT_SET", None, ""),
0x00000700: ("PL_LOGINFO_SUB_CODE_SATA_READ_LOG_RECEIVE_DATA_ERR", None, ""),
0x00000800: ("PL_LOGINFO_SUB_CODE_SATA_NCQ_FAIL_ALL_CMDS_AFTR_ERR", None, ""),
0x00000900: ("PL_LOGINFO_SUB_CODE_SATA_ERR_IN_RCV_SET_DEV_BIT_FIS", None, ""),
0x00000A00: ("PL_LOGINFO_SUB_CODE_RX_FM_INVALID_MESSAGE", None, ""),
0x00000B00: ("PL_LOGINFO_SUB_CODE_RX_CTX_MESSAGE_VALID_ERROR", None, ""),
0x00000C00: ("PL_LOGINFO_SUB_CODE_RX_FM_CURRENT_FRAME_ERROR", None, ""),
0x00000D00: ("PL_LOGINFO_SUB_CODE_SATA_LINK_DOWN", None, ""),
0x00000E00: ("PL_LOGINFO_SUB_CODE_DISCOVERY_SATA_ERR", None, ""),
0x00000F00: ("PL_LOGINFO_SUB_CODE_SECOND_OPEN", None, ""),
0x00001000: ("PL_LOGINFO_SUB_CODE_DSCVRY_SATA_INIT_TIMEOUT", None, ""),
0x00002000: ("PL_LOGINFO_SUB_CODE_BREAK_ON_SATA_CONNECTION", None, ""),
0x00003000: ("PL_LOGINFO_SUB_CODE_BREAK_ON_STUCK_LINK", None, ""),
0x00004000: ("PL_LOGINFO_SUB_CODE_BREAK_ON_STUCK_LINK_AIP", None, ""),
0x00005000: ("PL_LOGINFO_SUB_CODE_BREAK_ON_INCOMPLETE_BREAK_RCVD", None, ""),
}]

pl_config_err = ["Sub Code", 0x0000FFFF, {
0x00000000: ("PL_LOGIN0O_CODE_CON0IG_INVALID_PAGE", None, ""),
0x00000001: ("PL_LOGIN0O_CODE_CON0IG_PL_NOT_INITIALIZED", None, "PL not yet initialized, can't do config page req."),
0x00000100: ("PL_LOGIN0O_CODE_CON0IG_INVALID_PAGE_PT", None, "Invalid Page Type"),
0x00000200: ("PL_LOGIN0O_CODE_CON0IG_INVALID_PAGE_NUM_PHYS", None, "Invalid Number of Phys"),
0x00000300: ("PL_LOGIN0O_CODE_CON0IG_INVALID_PAGE_NOT_IMP", None, "Case Not Handled"),
0x00000400: ("PL_LOGIN0O_CODE_CON0IG_INVALID_PAGE_NO_DEV", None, "No Device 0ound"),
0x00000500: ("PL_LOGIN0O_CODE_CON0IG_INVALID_PAGE_0ORM", None, "Invalid 0ORM"),
0x00000600: ("PL_LOGIN0O_CODE_CON0IG_INVALID_PAGE_PHY", None, "Invalid Phy"),
0x00000700: ("PL_LOGIN0O_CODE_CON0IG_INVALID_PAGE_NO_OWNER", None, "No Owner 0ound"),
}]

pl_encl_mgmt_err = ["Sub Code", 0x0000FFFF, {
0x00000000: ("PL_LOGINFO_CODE_ENCL_MGMT_SMP_FRAME_FAILURE", None, "Can't get SMP Frame"),
0x00000010: ("PL_LOGINFO_CODE_ENCL_MGMT_SMP_READ_ERROR", None, "Error occured on SMP Read"),
0x00000010: ("PL_LOGINFO_CODE_ENCL_MGMT_SMP_READ_ERROR", None, "Error occurred on SMP Read"),
0x00000020: ("PL_LOGINFO_CODE_ENCL_MGMT_SMP_WRITE_ERROR", None, "Error occured on SMP Write"),
0x00000020: ("PL_LOGINFO_CODE_ENCL_MGMT_SMP_WRITE_ERROR", None, "Error occurred on SMP Write"),
0x00000040: ("PL_LOGINFO_CODE_ENCL_MGMT_NOT_SUPPORTED_ON_ENCL", None, "Encl Mgmt services not available for this WWID"),
0x00000050: ("PL_LOGINFO_CODE_ENCL_MGMT_ADDR_MODE_NOT_SUPPORTED", None, "Address Mode not suppored"),
0x00000060: ("PL_LOGINFO_CODE_ENCL_MGMT_BAD_SLOT_NUM", None, "Invalid Slot Number in SEP Msg"),
0x00000070: ("PL_LOGINFO_CODE_ENCL_MGMT_SGPIO_NOT_PRESENT", None, "SGPIO not present/enabled"),
0x00000080: ("PL_LOGINFO_CODE_ENCL_MGMT_GPIO_NOT_CONFIGURED", None, "GPIO not configured"),
0x00000090: ("PL_LOGINFO_CODE_ENCL_MGMT_GPIO_FRAME_ERROR", None, "GPIO can't allocate a frame"),
0x000000A0: ("PL_LOGINFO_CODE_ENCL_MGMT_GPIO_CONFIG_PAGE_ERROR", None, "GPIO failed config page request"),
0x000000B0: ("PL_LOGINFO_CODE_ENCL_MGMT_SES_FRAME_ALLOC_ERROR", None, "Can't get frame for SES command"),
0x000000C0: ("PL_LOGINFO_CODE_ENCL_MGMT_SES_IO_ERROR", None, "I/O execution error"),
0x000000D0: ("PL_LOGINFO_CODE_ENCL_MGMT_SES_RETRIES_EXHAUSTED", None, "SEP I/O retries exhausted"),
0x000000E0: ("PL_LOGINFO_CODE_ENCL_MGMT_SMP_FRAME_ALLOC_ERROR", None, "Can't get frame for SMP command"),
0x00000100: ("PL_LOGINFO_DA_SEP_NOT_PRESENT", None, "SEP not present when msg received"),
0x00000101: ("PL_LOGINFO_DA_SEP_SINGLE_THREAD_ERROR", None, "Can only accept 1 msg at a time"),
0x00000102: ("PL_LOGINFO_DA_SEP_ISTWI_INTR_IN_IDLE_STATE", None, "ISTWI interrupt recvd. while IDLE"),
0x00000103: ("PL_LOGINFO_DA_SEP_RECEIVED_NACK_FROM_SLAVE", None, "SEP NACK'd, it is busy"),
0x00000104: ("PL_LOGINFO_DA_SEP_DID_NOT_RECEIVE_ACK", None, "SEP didn't rcv. ACK (Last Rcvd Bit = 1)"),
0x00000105: ("PL_LOGINFO_DA_SEP_BAD_STATUS_HDR_CHKSUM", None, "SEP stopped or sent bad chksum in Hdr"),
0x00000106: ("PL_LOGINFO_DA_SEP_STOP_ON_DATA", None, "SEP stopped while transfering data"),
0x00000106: ("PL_LOGINFO_DA_SEP_STOP_ON_DATA", None, "SEP stopped while transferring data"),
0x00000107: ("PL_LOGINFO_DA_SEP_STOP_ON_SENSE_DATA", None, "SEP stopped while transfering sense data"),
0x00000107: ("PL_LOGINFO_DA_SEP_STOP_ON_SENSE_DATA", None, "SEP stopped while transferring sense data"),
0x00000108: ("PL_LOGINFO_DA_SEP_UNSUPPORTED_SCSI_STATUS_1", None, "SEP returned unknown scsi status"),
0x00000109: ("PL_LOGINFO_DA_SEP_UNSUPPORTED_SCSI_STATUS_2", None, "SEP returned unknown scsi status"),
0x0000010A: ("PL_LOGINFO_DA_SEP_CHKSUM_ERROR_AFTER_STOP", None, "SEP returned bad chksum after STOP"),
0x0000010B: ("PL_LOGINFO_DA_SEP_CHKSUM_ERROR_AFTER_STOP_GETDATA", None, "SEP returned bad chksum after STOP while gettin data"),
0x0000010C: ("PL_LOGINFO_DA_SEP_UNSUPPORTED_COMMAND", None, "SEP doesn't support CDB opcode f/w location 1"),
0x0000010D: ("PL_LOGINFO_DA_SEP_UNSUPPORTED_COMMAND_2", None, "SEP doesn't support CDB opcode f/w location 2"),
0x0000010E: ("PL_LOGINFO_DA_SEP_UNSUPPORTED_COMMAND_3", None, "SEP doesn't support CDB opcode f/w location 3"),
}]

pl_code = ["Code", 0x00FF0000, {
0x00010000: ("PL_LOGINFO_CODE_OPEN_FAILURE", pl_open_fail, "see SUB_CODE_OPEN_FAIL_ below"),
0x00020000: ("PL_LOGINFO_CODE_INVALID_SGL", None, ""),
0x00030000: ("PL_LOGINFO_CODE_WRONG_REL_OFF_OR_FRAME_LENGTH", None, ""),
0x00040000: ("PL_LOGINFO_CODE_FRAME_XFER_ERROR", None, ""),
0x00050000: ("PL_LOGINFO_CODE_TX_FM_CONNECTED_LOW", None, ""),
0x00060000: ("PL_LOGINFO_CODE_SATA_NON_NCQ_RW_ERR_BIT_SET", None, ""),
0x00070000: ("PL_LOGINFO_CODE_SATA_READ_LOG_RECEIVE_DATA_ERR", None, ""),
0x00080000: ("PL_LOGINFO_CODE_SATA_NCQ_FAIL_ALL_CMDS_AFTR_ERR", None, ""),
0x00090000: ("PL_LOGINFO_CODE_SATA_ERR_IN_RCV_SET_DEV_BIT_FIS", None, ""),
0x000A0000: ("PL_LOGINFO_CODE_RX_FM_INVALID_MESSAGE", None, ""),
0x000B0000: ("PL_LOGINFO_CODE_RX_CTX_MESSAGE_VALID_ERROR", None, ""),
0x000C0000: ("PL_LOGINFO_CODE_RX_FM_CURRENT_FRAME_ERROR", None, ""),
0x000D0000: ("PL_LOGINFO_CODE_SATA_LINK_DOWN", None, ""),
0x000E0000: ("PL_LOGINFO_CODE_DISCOVERY_SATA_INIT_W_IOS", None, ""),
0x000F0000: ("PL_LOGINFO_CODE_CONFIG_ERROR", pl_config_err, ""),
0x00100000: ("PL_LOGINFO_CODE_DSCVRY_SATA_INIT_TIMEOUT", None, ""),
0x00110000: ("PL_LOGINFO_CODE_RESET", pl_open_fail, "See Sub-Codes below (PL_LOGINFO_SUB_CODE)"),
0x00120000: ("PL_LOGINFO_CODE_ABORT", pl_open_fail, "See Sub-Codes below (PL_LOGINFO_SUB_CODE)"),
0x00130000: ("PL_LOGINFO_CODE_IO_NOT_YET_EXECUTED", None, "Associated with Task Abort"),
0x00140000: ("PL_LOGINFO_CODE_IO_EXECUTED", None, "Associated with Task Abort"),
0x00150000: ("PL_LOGINFO_CODE_PERS_RESV_OUT_NOT_AFFIL_OWNER", None, ""),
0x00160000: ("PL_LOGINFO_CODE_OPEN_TXDMA_ABORT", None, ""),
0x00170000: ("PL_LOGINFO_CODE_IO_DEVICE_MISSING_DELAY_RETRY", None, "I-T Nexus Loss"),
0x00180000: ("PL_LOGINFO_CODE_IO_CANCELLED_DUE_TO_R_ERR", None, ""),
0x00200000: ("PL_LOGINFO_CODE_ENCL_MGMT_ERR", pl_encl_mgmt_err, ""),
}]

type_sas = ["Origin", 0x0F000000, {
            0x00000000: ('IOP', iop_code, ""),
            0x01000000: ('PL', pl_code, ""),
            0x02000000: ('IR', ir_code, ""),
}]

fc_initiator = ["Code", 0x00FFFFFF, {
0x00000000: ('BASE', None, ''),
0x00000001: ('ERROR_OUT_OF_ORDER_FRAME', None, 'received an out of order frame - unsupported'),
0x00000002: ('ERROR_BAD_START_OF_FRAME', None, 'Bad Rx Frame, bad start of frame primative'),
0x00000003: ('ERROR_BAD_END_OF_FRAME', None, 'Bad Rx Frame, bad end of frame primative'),
0x00000004: ('ERROR_OVER_RUN', None, 'Bad Rx Frame, overrun'),
0x00000005: ('ERROR_RX_OTHER', None, 'Other errors caught by IOC which require retries'),
0x00000006: ('ERROR_SUBPROC_DEAD', None, 'Main processor could not initialize sub-processor'),
0x00000007: ('ERROR_RX_OVERRUN', None, 'Scatter Gather overrun '),
0x00000008: ('ERROR_RX_BAD_STATUS', None, 'Receiver detected context mismatch via invalid header'),
0x00000009: ('ERROR_RX_UNEXPECTED_FRAME', None, 'CtxMgr detected unsupported frame type '),
0x0000000A: ('ERROR_LINK_FAILURE', None, 'Link failure occurred '),
0x0000000B: ('ERROR_TX_TIMEOUT', None, 'Transmitter timeout error'),
}]

fc_target = ["Code", 0x00FFFFFF, {
0x00000000: ('BASE', None, ''),
0x00000001: ('NO_PDISC', None, 'not sent because we are waiting for a PDISC from the initiator'),
0x00000002: ('NO_LOGIN', None, 'not sent because we are not logged in to the remote node'),
0x00000003: ('DOAR_KILLED_BY_LIP', None, 'Data Out, Auto Response, not sent due to a LIP'),
0x00000004: ('DIAR_KILLED_BY_LIP', None, 'Data In, Auto Response, not sent due to a LIP'),
0x00000005: ('DIAR_MISSING_DATA', None, 'Data In, Auto Response, missing data frames'),
0x00000006: ('DONR_KILLED_BY_LIP', None, 'Data Out, No Response, not sent due to a LIP'),
0x00000007: ('WRSP_KILLED_BY_LIP', None, 'Auto-response after a write not sent due to a LIP'),
0x00000008: ('DINR_KILLED_BY_LIP', None, 'Data In, No Response, not completed due to a LIP'),
0x00000009: ('DINR_MISSING_DATA', None, 'Data In, No Response, missing data frames'),
0x0000000a: ('MRSP_KILLED_BY_LIP', None, 'Manual Response not sent due to a LIP'),
0x0000000b: ('NO_CLASS_3', None, 'not sent because remote node does not support Class 3'),
0x0000000c: ('LOGIN_NOT_VALID', None, 'not sent because login to remote node not validated'),
0x0000000e: ('FROM_OUTBOUND', None, 'cleared from the outbound queue after a logout'),
0x0000000f: ('WAITING_FOR_DATA_IN', None, 'cleared waiting for data after a logout'),
}]

fc_lan = ["Code", 0x00FFFFFF, {
0x00000000: ('BASE', None, ''),
0x00000001: ('TRANS_SGL_MISSING', None, 'Transaction Context Sgl Missing'),
0x00000002: ('TRANS_WRONG_PLACE', None, 'Transaction Context found before an EOB'),
0x00000003: ('TRANS_RES_BITS_SET', None, 'Transaction Context value has reserved bits set'),
0x00000004: ('WRONG_SGL_FLAG', None, 'Invalid SGL Flags'),
}]

fc_link = ["Code", 0x00FFFFFF, {
0x00000000: ('BASE', None, ''),
0x00000001: ('LOOP_INIT_TIMEOUT', None, 'Loop initialization timed out'),
0x00000002: ('ALREADY_INITIALIZED', None, 'Another system controller already initialized the loop'),
0x00000003: ('NOT_ESTABLISHED', None, 'Not synchronized to signal or still negotiating (possible cable problem)'),
0x00000004: ('CRC_ERROR', None, 'CRC check detected error on received frame'),
}]

# TODO: For FC 0x26000000 the 6 nibbles at the end give the invalid byte offset
# TODO: For FC 0x27000000 the 6 nibbles give additional information concerning state change

type_fc = ["Origin", 0x0F000000, {
    0x00000000: ('FCP Initiator', fc_initiator, ''),
    0x01000000: ('FCP Target', fc_target, ""),
    0x02000000: ('LAN', fc_lan, ""),
    0x03000000: ('MPI Message Layer', None, ""),
    0x04000000: ('FC Link', None, ""),
    0x05000000: ('Context Manager', None, ""),
    0x06000000: ('Invalid Field Offset', None, ""),
    0x07000000: ('State Change Info', None, ""),
}]

types = ["Type", 0xF0000000, {
         0x00000000: ('NONE', None, ""),
         0x10000000: ('SCSI', None, ""),
         0x20000000: ('FC', type_fc, ""),
         0x30000000: ('SAS', type_sas, ""),
         0x40000000: ('iSCSI', None, ""),
}]

def _decode_lsi_loginfo(d, val, unparsed):
    if d is None:
        return unparsed

    name = d[0]
    mask = d[1]
    vals = d[2]

    masked_val = mask & val
    unparsed = unparsed & ~mask

    info = vals.get(masked_val, None)
    name += ':'
    if info is not None:
        print '%-10s\t%08Xh\t%s %s' % (name, masked_val, info[0], info[2])
        return _decode_lsi_loginfo(info[1], val, unparsed)
    else:
        print '%-10s\t%08Xh\tUnknown code' % (name, masked_val)
        return unparsed

def decode_lsi_loginfo(val):
    print '%-10s\t%08Xh' % ('Value', val)
    unparsed = _decode_lsi_loginfo(types, val, val)
    if unparsed:
        print '%-10s\t%08Xh' % ('Unparsed', unparsed)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Must provide a loginfo number to decode, as in:'
        print '%s 0x31120000' % sys.argv[0]
        sys.exit(1)
    
    try:
        val = int(sys.argv[1], 0)
    except ValueError:
        print 'Failure to parse the value "%s", it must be a number' % sys.argv[1]
        sys.exit(1)

    decode_lsi_loginfo(val)
