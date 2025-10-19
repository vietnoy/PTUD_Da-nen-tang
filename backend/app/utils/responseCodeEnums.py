from enum import Enum


class ResponseCode(Enum):
    """Enum chứa tất cả các mã lỗi và thông báo tương ứng"""

    # Authentication & Authorization Errors (00005-00024)
    MISSING_INFORMATION = ("00005", "Vui lòng cung cấp đầy đủ thông tin để gửi mã.")
    ACCESS_DENIED_NO_TOKEN = (
        "00006",
        "Truy cập bị từ chối. Không có token được cung cấp.",
    )
    INVALID_USER_ID = ("00007", "ID người dùng không hợp lệ.")
    INTERNAL_SERVER_ERROR = ("00008", "Đã xảy ra lỗi máy chủ nội bộ, vui lòng thử lại.")
    USER_NOT_FOUND_VERIFICATION = (
        "00009",
        "Không thể tìm thấy người dùng đã xác minh với mã và ID được cung cấp. Hãy đảm bảo rằng tài khoản đã được xác minh và kích hoạt.",
    )
    SESSION_EXPIRED = ("00011", "Phiên của bạn đã hết hạn, vui lòng đăng nhập lại.")
    INVALID_TOKEN = ("00012", "Token không hợp lệ. Token có thể đã hết hạn.")
    ACCESS_DENIED_NO_PERMISSION_17 = (
        "00017",
        "Truy cập bị từ chối. Bạn không có quyền truy cập.",
    )
    ACCESS_DENIED_NO_PERMISSION_19 = (
        "00019",
        "Truy cập bị từ chối. Bạn không có quyền truy cập.",
    )
    ACCESS_DENIED_NO_PERMISSION_21 = (
        "00021",
        "Truy cập bị từ chối. Bạn không có quyền truy cập.",
    )
    MISSING_ID_PARAMETER = (
        "00022",
        "Không có ID được cung cấp trong tham số. Vui lòng nhập một ID.",
    )
    INVALID_OBJECT_ID = (
        "00023",
        "ID được cung cấp không phải là một đối tượng ID hợp lệ.",
    )
    TOO_MANY_REQUESTS = ("00024", "Quá nhiều yêu cầu.")

    # Validation Errors (00025-00032)
    MISSING_REQUIRED_FIELDS = ("00025", "Vui lòng cung cấp tất cả các trường bắt buộc!")
    INVALID_EMAIL_26 = ("00026", "Vui lòng cung cấp một địa chỉ email hợp lệ!")
    INVALID_PASSWORD_LENGTH = (
        "00027",
        "Vui lòng cung cấp mật khẩu dài hơn 6 ký tự và ngắn hơn 20 ký tự.",
    )
    INVALID_NAME_LENGTH = (
        "00028",
        "Vui lòng cung cấp một tên dài hơn 3 ký tự và ngắn hơn 30 ký tự.",
    )
    INVALID_EMAIL_29 = ("00029", "Vui lòng cung cấp một địa chỉ email hợp lệ!")
    EMAIL_ALREADY_EXISTS = ("00032", "Một tài khoản với địa chỉ email này đã tồn tại.")

    # Registration & Login (00035-00050)
    REGISTRATION_SUCCESS = ("00035", "Bạn đã đăng ký thành công.")
    EMAIL_NOT_FOUND_36 = ("00036", "Không tìm thấy tài khoản với địa chỉ email này.")
    MISSING_REQUIRED_FIELDS_38 = (
        "00038",
        "Vui lòng cung cấp tất cả các trường bắt buộc!",
    )
    INVALID_EMAIL_39 = ("00039", "Vui lòng cung cấp một địa chỉ email hợp lệ!")
    INVALID_PASSWORD_LENGTH_40 = (
        "00040",
        "Vui lòng cung cấp mật khẩu dài hơn 6 ký tự và ngắn hơn 20 ký tự.",
    )
    EMAIL_NOT_FOUND_42 = ("00042", "Không tìm thấy tài khoản với địa chỉ email này.")
    EMAIL_NOT_ACTIVATED = (
        "00043",
        "Email của bạn chưa được kích hoạt, vui lòng đăng ký trước.",
    )
    EMAIL_NOT_VERIFIED = (
        "00044",
        "Email của bạn chưa được xác minh, vui lòng xác minh email của bạn.",
    )
    INVALID_EMAIL_OR_PASSWORD = (
        "00045",
        "Bạn đã nhập một email hoặc mật khẩu không hợp lệ.",
    )
    LOGIN_SUCCESS = ("00047", "Bạn đã đăng nhập thành công.")
    CODE_SENT_SUCCESS = ("00048", "Mã đã được gửi đến email của bạn thành công.")
    LOGOUT_SUCCESS = ("00050", "Đăng xuất thành công.")

    # User Management (00052-00092)
    USER_NOT_FOUND_52 = ("00052", "Không thể tìm thấy người dùng.")
    MISSING_VERIFICATION_CODE = ("00053", "Vui lòng gửi một mã xác nhận.")
    VERIFICATION_CODE_MISMATCH = (
        "00054",
        "Mã bạn nhập không khớp với mã chúng tôi đã gửi đến email của bạn. Vui lòng kiểm tra lại.",
    )
    INVALID_TOKEN_55 = ("00055", "Token không hợp lệ. Token có thể đã hết hạn.")
    EMAIL_VERIFIED_SUCCESS = (
        "00058",
        "Địa chỉ email của bạn đã được xác minh thành công.",
    )
    MISSING_REFRESH_TOKEN = ("00059", "Vui lòng cung cấp token làm mới.")
    TOKEN_USER_MISMATCH = (
        "00061",
        "Token được cung cấp không khớp với người dùng, vui lòng đăng nhập.",
    )
    TOKEN_EXPIRED = ("00062", "Token đã hết hạn, vui lòng đăng nhập.")
    TOKEN_VERIFICATION_FAILED = (
        "00063",
        "Không thể xác minh token, vui lòng đăng nhập.",
    )
    TOKEN_REFRESH_SUCCESS = ("00065", "Token đã được làm mới thành công.")
    INVALID_PASSWORD_LENGTH_66 = (
        "00066",
        "Vui lòng cung cấp một mật khẩu dài hơn 6 và ngắn hơn 20 ký tự.",
    )
    NEW_PASSWORD_CREATED = ("00068", "Mật khẩu mới đã được tạo thành công.")
    INVALID_OLD_NEW_PASSWORD = (
        "00069",
        "Vui lòng cung cấp mật khẩu cũ và mới dài hơn 6 ký tự và ngắn hơn 20 ký tự.",
    )
    OLD_PASSWORD_MISMATCH = (
        "00072",
        "Mật khẩu cũ của bạn không khớp với mật khẩu bạn nhập, vui lòng nhập mật khẩu đúng.",
    )
    PASSWORD_SAME_AS_OLD = (
        "00073",
        "Mật khẩu mới của bạn không nên giống với mật khẩu cũ, vui lòng thử một mật khẩu khác.",
    )
    PASSWORD_CHANGED_SUCCESS = (
        "00076",
        "Mật khẩu của bạn đã được thay đổi thành công.",
    )
    INVALID_NAME_LENGTH_77 = (
        "00077",
        "Vui lòng cung cấp một tên dài hơn 3 ký tự và ngắn hơn 30 ký tự.",
    )
    INVALID_GENDER_OPTIONS = (
        "00078",
        "Các tùy chọn giới tính hợp lệ, female-male-other, vui lòng cung cấp một trong số chúng.",
    )
    INVALID_LANGUAGE_OPTIONS = (
        "00079",
        "Các tùy chọn ngôn ngữ hợp lệ, tr-en, vui lòng cung cấp một trong số chúng.",
    )
    INVALID_DATE_OF_BIRTH = ("00080", "Vui lòng cung cấp một ngày sinh hợp lệ.")
    INVALID_USERNAME_LENGTH = (
        "00081",
        "Vui lòng cung cấp một tên người dùng dài hơn 3 ký tự và ngắn hơn 15 ký tự.",
    )
    USERNAME_ALREADY_EXISTS = (
        "00084",
        "Đã có một người dùng với tên người dùng này, vui lòng nhập tên khác.",
    )
    PROFILE_UPDATED_SUCCESS = (
        "00086",
        "Thông tin hồ sơ của bạn đã được thay đổi thành công.",
    )
    USER_INFO_RETRIEVED = ("00089", "Thông tin người dùng đã được lấy thành công.")
    ACCOUNT_DELETED_SUCCESS = ("00092", "Tài khoản của bạn đã bị xóa thành công.")

    # Group Management (00093-00110)
    CANNOT_CREATE_GROUP_ALREADY_IN_GROUP = (
        "00093",
        "Không thể tạo nhóm, bạn đã thuộc về một nhóm rồi",
    )
    GROUP_CREATED_SUCCESS = ("00095", "Tạo nhóm thành công")
    USER_NOT_IN_GROUP = ("00096", "Bạn không thuộc về nhóm nào")
    SUCCESS_98 = ("00098", "Thành công")
    USER_ALREADY_IN_GROUP = ("00099", "Người này đã thuộc về một nhóm")
    USER_NOT_EXISTS = ("00099x", "Không tồn tại user này")
    MISSING_USERNAME_100 = ("00100", "Thiếu username")
    USER_ADDED_TO_GROUP_SUCCESS = ("00102", "Người dùng thêm vào nhóm thành công")
    USER_NOT_IN_ANY_GROUP = ("00103", "Người này chưa vào nhóm nào")
    NOT_ADMIN_CANNOT_DELETE = ("00104", "Bạn không phải admin, không thể xóa")
    DELETE_SUCCESS_106 = ("00106", "Xóa thành công")
    MISSING_USERNAME_107 = ("00107", "Thiếu username")
    SYSTEM_LOG_SUCCESS = ("00109", "Lấy log hệ thống thành công")
    GET_UNITS_SUCCESS = ("00110", "Lấy các unit thành công")

    # Unit Management (00112-00128)
    MISSING_UNIT_NAME = ("00112", "Thiếu thông tin tên của đơn vị")
    UNIT_NAME_EXISTS = ("00113", "Đã tồn tại đơn vị có tên này")
    SERVER_ERROR_114 = ("00114", "server error")
    SERVER_ERROR_115 = ("00115", "server error")
    CREATE_UNIT_SUCCESS = ("00116", "Tạo đơn vị thành công")
    MISSING_OLD_NEW_NAME = ("00117", "Thiếu thông tin name cũ, name mới")
    OLD_NAME_SAME_AS_NEW = ("00118", "Tên cũ trùng với tên mới")
    UNIT_NOT_FOUND_119 = ("00119", "Không tìm thấy đơn vị với tên cung cấp")
    SERVER_ERROR_120 = ("00120", "server error")
    SERVER_ERROR_121 = ("00121", "server error")
    UPDATE_UNIT_SUCCESS = ("00122", "Sửa đổi đơn vị thành công")
    MISSING_UNIT_NAME_123 = ("00123", "Thiếu thông tin tên của đơn vị")
    UNIT_NOT_FOUND_125 = ("00125", "Không tìm thấy đơn vị với tên cung cấp")
    SERVER_ERROR_126 = ("00126", "server error")
    SERVER_ERROR_127 = ("00127", "server error")
    DELETE_UNIT_SUCCESS = ("00128", "Xóa đơn vị thành công")

    # Category Management (00129-00146)
    GET_CATEGORIES_SUCCESS = ("00129", "Lấy các category thành công")
    MISSING_CATEGORY_NAME_131 = ("00131", "Thiếu thông tin tên của category")
    CATEGORY_NAME_EXISTS = ("00132", "Đã tồn tại category có tên này")
    SERVER_ERROR_133 = ("00133", "server error")
    SERVER_ERROR_134 = ("00134", "server error")
    CREATE_CATEGORY_SUCCESS = ("00135", "Tạo category thành công")
    MISSING_OLD_NEW_CATEGORY_NAME = ("00136", "Thiếu thông tin name cũ, name mới")
    OLD_CATEGORY_NAME_SAME_AS_NEW = ("00137", "Tên cũ trùng với tên mới")
    CATEGORY_NOT_FOUND_138 = ("00138", "Không tìm thấy category với tên cung cấp")
    NEW_CATEGORY_NAME_EXISTS = ("00138x", "Tên mới đã tồn tại")
    SERVER_ERROR_139 = ("00139", "server error")
    SERVER_ERROR_140 = ("00140", "server error")
    UPDATE_CATEGORY_SUCCESS = ("00141", "Sửa đổi category thành công")
    MISSING_CATEGORY_NAME_142 = ("00142", "Thiếu thông tin tên của category")
    CATEGORY_NOT_FOUND_143 = ("00143", "Không tìm thấy category với tên cung cấp")
    SERVER_ERROR_144 = ("00144", "server error")
    SERVER_ERROR_145 = ("00145", "server error")
    DELETE_CATEGORY_SUCCESS = ("00146", "Xóa category thành công")

    # Food Management (00147-00188)
    MISSING_REQUIRED_FIELDS_147 = (
        "00147",
        "Vui lòng cung cấp tất cả các trường bắt buộc!",
    )
    INVALID_FOOD_NAME = ("00148", "Vui lòng cung cấp tên của thực phẩm hợp lệ!")
    MISSING_FOOD_CATEGORY = (
        "00149",
        "Vui lòng cung cấp tên của category của thực phẩm",
    )
    MISSING_FOOD_UNIT = ("00150", "Vui lòng cung cấp tên đơn vị đo của thực phẩm")
    FOOD_NAME_EXISTS = ("00151", "Đã tồn tại thức ăn với tên này")
    SERVER_ERROR_152 = ("00152", "server error")
    UNIT_NOT_FOUND_153 = ("00153", "Không tìm thấy đơn vị với tên cung cấp")
    SERVER_ERROR_154 = ("00154", "server error")
    CATEGORY_NOT_FOUND_155 = ("00155", "Không tìm thấy category với tên cung cấp")
    MUST_JOIN_GROUP_TO_CREATE_FOOD = ("00156x", "Hãy vào nhóm trước để tạo thực phẩm")
    SERVER_ERROR_157 = ("00157", "server error")
    IMAGE_UPLOAD_FAILED = ("00158", "đăng tải ảnh thất bại")
    SERVER_ERROR_159 = ("00159", "server error")
    CREATE_FOOD_SUCCESS = ("00160", "Tạo thực phẩm thành công")
    MISSING_REQUIRED_FIELDS_161 = (
        "00161",
        "Vui lòng cung cấp tất cả các trường bắt buộc!",
    )
    INVALID_FOOD_NAME_162 = ("00162", "Vui lòng cung cấp tên thực phẩm hợp lệ!")
    MISSING_UPDATE_FIELDS = (
        "00163",
        "Vui lòng cung cấp ít nhất một trong các trường sau, newName, newCategory, newUnit",
    )
    INVALID_NEW_CATEGORY = (
        "00164",
        "Vui lòng cung cấp một danh mục mới hợp lệ cho thực phẩm",
    )
    INVALID_NEW_UNIT = (
        "00165",
        "Vui lòng cung cấp một đơn vị mới hợp lệ cho thực phẩm",
    )
    INVALID_NEW_FOOD_NAME = (
        "00166",
        "Vui lòng cung cấp một tên mới hợp lệ cho thực phẩm",
    )
    FOOD_NOT_EXISTS = ("00167", "Thực phẩm với tên đã cung cấp không tồn tại")
    NO_EDIT_PERMISSION = ("00167x", "Bạn không có quyền chỉnh sửa")
    SERVER_ERROR_168 = ("00168", "server error")
    UNIT_NOT_FOUND_169 = ("00169", "Không tìm thấy đơn vị với tên đã cung cấp")
    CATEGORY_NOT_FOUND_171 = ("00171", "Không tìm thấy danh mục với tên đã cung cấp")
    FOOD_NAME_ALREADY_EXISTS = ("00173", "Một thực phẩm với tên này đã tồn tại")
    SUCCESS_178 = ("00178", "Thành công")
    MISSING_FOOD_NAME_179 = ("00179", "Vui lòng cung cấp tên thực phẩm")
    FOOD_NOT_FOUND_180 = ("00180", "Không tìm thấy thực phẩm với tên đã cung cấp")
    NO_PERMISSION_181 = ("00181", "Bạn không có quyền")
    DELETE_FOOD_SUCCESS = ("00184", "Xóa thực phẩm thành công")
    USER_NOT_IN_GROUP_185 = ("00185", "Bạn chưa vào nhóm nào")
    GET_FOOD_LIST_SUCCESS = ("00188", "Lấy danh sách thực phẩm thành công")

    # Refrigerator Management (00190-00237)
    INVALID_FOOD_NAME_190 = ("00190", "Vui lòng cung cấp một tên thực phẩm hợp lệ!")
    INVALID_USE_WITHIN_VALUE = (
        "00191",
        "Vui lòng cung cấp một giá trị 'sử dụng trong khoảng' hợp lệ!",
    )
    INVALID_QUANTITY = ("00192", "Vui lòng cung cấp một số lượng hợp lệ!")
    INVALID_NOTE_FORMAT = ("00193", "Định dạng ghi chú không hợp lệ!")
    FOOD_NOT_EXISTS_194 = ("00194", "Thực phẩm không tồn tại.")
    USER_NO_GROUP_PERMISSION = (
        "00196",
        "Người dùng không có quyền do không thuộc nhóm.",
    )
    FOOD_NOT_BELONG_TO_GROUP = (
        "00198",
        "Thực phẩm không thuộc quyền quản trị của nhóm.",
    )
    FRIDGE_ITEM_EXISTS = ("00199", "Mục trong tủ lạnh cho thực phẩm đã tồn tại.")
    CREATE_FRIDGE_ITEM_SUCCESS = ("00202", "Mục trong tủ lạnh được tạo thành công.")
    MISSING_REQUIRED_FIELDS_203 = ("00203", "Vui cung cấp tất cả các trường cần thiết")
    MISSING_FRIDGE_ITEM_ID = ("00204", "Vui lòng cung cấp id của item tủ lạnh")
    MISSING_UPDATE_FIELDS_204X = (
        "00204x",
        "Vui lòng cung cấp ít nhất một trong các trường sau, newQuantity, newNote, newUseWithin",
    )
    INVALID_USE_WITHIN_205 = (
        "00205",
        "Vui lòng cung cấp một giá trị 'sử dụng trong' hợp lệ!",
    )
    INVALID_QUANTITY_206 = ("00206", "Vui lòng cung cấp một lượng hợp lệ!")
    INVALID_NEW_NOTE_FORMAT = ("00207", "Định dạng ghi chú mới không hợp lệ!")
    INVALID_NEW_FOOD_NAME_FORMAT = ("00207", "Định dạng tên thức ăn mới không hợp lệ!")
    FOOD_NOT_EXISTS_208 = ("00208", "Thực phẩm không tồn tại.")
    USER_NOT_IN_ANY_GROUP_210 = ("00210", "Người dùng không thuộc bất kỳ nhóm nào")
    FRIDGE_NOT_BELONG_TO_GROUP_ADMIN = (
        "00212",
        "Tủ lạnh không thuộc quản trị viên nhóm.",
    )
    FRIDGE_ITEM_NOT_EXISTS = ("00213", "Mục tủ lạnh không tồn tại.")
    NEW_FOOD_NAME_NOT_EXISTS = ("00214x", "Tên thực phẩm mới không tồn tại")
    UPDATE_FRIDGE_ITEM_SUCCESS = ("00216", "Cập nhật mục tủ lạnh thành công.")
    MISSING_FOOD_NAME_217 = ("00217", "Vui lòng cung cấp tên thực phẩm")
    FOOD_NOT_FOUND_218 = ("00218", "Không tìm thấy thực phẩm với tên đã cung cấp")
    NO_PERMISSION_219 = ("00219", "Bạn không có quyền")
    FRIDGE_ITEM_NOT_CREATED = (
        "00221",
        "Mục trong tủ lạnh liên kết với thực phẩm này chưa được tạo",
    )
    DELETE_FRIDGE_ITEM_SUCCESS = ("00224", "Xóa mục trong tủ lạnh thành công")
    USER_NOT_IN_GROUP_225 = ("00225", "Bạn chưa vào nhóm nào")
    GET_FRIDGE_LIST_SUCCESS = ("00228", "Lấy danh sách đồ tủ lạnh thành công")
    MISSING_FOOD_NAME_229 = ("00229", "Vui lòng cung cấp tên thực phẩm")
    FOOD_NOT_FOUND_230 = ("00230", "Không tìm thấy thực phẩm với tên đã cung cấp")
    NO_PERMISSION_232 = ("00232", "Bạn không có quyền")
    FRIDGE_ITEM_NOT_CREATED_234 = (
        "00234",
        "Mục trong tủ lạnh liên kết với thực phẩm này chưa được tạo",
    )
    GET_SPECIFIC_ITEM_SUCCESS = ("00237", "Lấy item cụ thể thành công")

    # Shopping List Management (00238-00312)
    MISSING_REQUIRED_FIELDS_238 = ("00238", "Vui cung cấp tất cả các trường cần thiết")
    MISSING_NAME_239 = ("00239", "Vui lòng cung cấp tên")
    MISSING_ASSIGN_USERNAME = ("00240", "Vui lòng cung cấp assignToUsername")
    INVALID_NOTE_FORMAT_241 = ("00241", "Định dạng ghi chú không hợp lệ")
    INVALID_DATE_FORMAT = ("00242", "Định dạng ngày không hợp lệ")
    UNAUTHORIZED_ACCESS_243 = (
        "00243",
        "Truy cập không được ủy quyền. Bạn không có quyền.",
    )
    ASSIGNED_USERNAME_NOT_EXISTS = ("00245", "Tên người dùng được gán không tồn tại.")
    UNAUTHORIZED_ASSIGN_SHOPPING_LIST = (
        "00246",
        "Truy cập không được ủy quyền. Bạn không có quyền gán danh sách mua sắm cho người dùng này.",
    )
    CREATE_SHOPPING_LIST_SUCCESS = (
        "00249",
        "Danh sách mua sắm đã được tạo thành công.",
    )
    MISSING_REQUIRED_FIELDS_250 = ("00250", "Vui cung cấp tất cả các trường cần thiết")
    MISSING_LIST_ID = ("00251", "Vui lòng cung cấp id danh sách")
    MISSING_UPDATE_FIELDS_252 = (
        "00252",
        "Vui lòng cung cấp ít nhất một trong những trường sau, newName, newAssignToUsername, newNote,newDate",
    )
    INVALID_NEW_NAME_FORMAT = ("00253", "Định dạng tên mới không hợp lệ")
    INVALID_NEW_ASSIGN_USERNAME = (
        "00254",
        "Định dạng tên người được giao mới không hợp lệ",
    )
    INVALID_NEW_NOTE_FORMAT_255 = ("00255", "Định dạng ghi chú mới không hợp lệ")
    INVALID_NEW_DATE_FORMAT = ("00256", "Định dạng ngày mới không hợp lệ")
    USER_NOT_GROUP_ADMIN_258 = ("00258", "Người dùng không phải là quản trị viên nhóm")
    SHOPPING_LIST_NOT_FOUND_260 = ("00260", "Không tìm thấy danh sách mua sắm")
    USER_NOT_SHOPPING_LIST_ADMIN = (
        "00261",
        "Người dùng không phải là quản trị viên của danh sách mua sắm này",
    )
    USER_NOT_EXISTS_262 = ("00262", "Người dùng không tồn tại")
    USER_NO_ASSIGN_PERMISSION = (
        "00263",
        "Người dùng không có quyền gán danh sách này cho tên người dùng",
    )
    UPDATE_SHOPPING_LIST_SUCCESS = ("00266", "Cập nhật danh sách mua sắm thành công")
    MISSING_REQUIRED_FIELDS_267 = ("00267", "Cung cấp các trường cần thiết")
    MISSING_LIST_ID_268 = ("00268", "Vui lòng cung cấp id danh sách")
    USER_NOT_GROUP_ADMIN_270 = ("00270", "Người dùng không phải là quản trị viên nhóm")
    SHOPPING_LIST_NOT_FOUND_272 = ("00272", "Không tìm thấy danh sách mua sắm")
    USER_NOT_SHOPPING_LIST_ADMIN_273 = (
        "00273",
        "Người dùng không phải là quản trị viên của danh sách mua sắm này",
    )
    DELETE_SHOPPING_LIST_SUCCESS = ("00275", "Xóa danh sách mua sắm thành công")
    MISSING_REQUIRED_FIELDS_276 = (
        "00276",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    MISSING_LIST_ID_277 = ("00277", "Vui lòng cung cấp một ID của danh sách")
    MISSING_TASKS_ARRAY = ("00278", "Vui lòng cung cấp một mảng nhiệm vụ")
    INVALID_TASKS_ARRAY = (
        "00279",
        "Vui lòng cung cấp một mảng nhiệm vụ với các trường hợp lệ",
    )
    USER_NOT_GROUP_ADMIN_281 = (
        "00281",
        "Người dùng không phải là quản trị viên của nhóm",
    )
    SHOPPING_LIST_NOT_FOUND_283 = ("00283", "Không tìm thấy danh sách mua sắm")
    USER_NOT_SHOPPING_LIST_ADMIN_284 = (
        "00284",
        "Người dùng không phải là quản trị viên của danh sách mua sắm này",
    )
    FOOD_NOT_FOUND_IN_ARRAY = (
        "00285",
        "Không tìm thấy một món ăn với tên cung cấp trong mảng",
    )
    FOOD_ALREADY_IN_LIST = ("00285x", "Loại thức ăn này đã có trong danh sách rồi")
    ADD_TASK_SUCCESS = ("00287", "Thêm nhiệm vụ thành công")
    USER_NOT_IN_GROUP_288 = ("00288", "Người dùng này chưa thuộc nhóm nào")
    GET_SHOPPING_LISTS_SUCCESS = ("00292", "Lấy danh sách các shopping list thành công")
    MISSING_REQUIRED_FIELDS_293 = (
        "00293",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    MISSING_TASK_ID = ("00294", "Vui lòng cung cấp một ID nhiệm vụ trong trường taskId")
    TASK_NOT_FOUND_296 = ("00296", "Không tìm thấy nhiệm vụ với ID đã cung cấp")
    USER_NOT_GROUP_ADMIN_297 = ("00297", "Người dùng không phải là quản trị viên nhóm")
    DELETE_TASK_SUCCESS = ("00299", "Xóa nhiệm vụ thành công")
    MISSING_REQUIRED_FIELDS_300 = (
        "00300",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    MISSING_TASK_ID_301 = (
        "00301",
        "Vui lòng cung cấp một ID nhiệm vụ trong trường taskId",
    )
    MISSING_UPDATE_TASK_FIELDS = (
        "00302",
        "Vui lòng cung cấp ít nhất một trong các trường sau, newFoodName, newQuantity",
    )
    INVALID_NEW_FOOD_NAME_303 = ("00303", "Vui lòng cung cấp một newFoodName hợp lệ")
    INVALID_NEW_QUANTITY = ("00304", "Vui lòng cung cấp một newQuantity hợp lệ")
    TASK_NOT_FOUND_306 = ("00306", "Không tìm thấy nhiệm vụ với ID đã cung cấp")
    USER_NOT_GROUP_ADMIN_307 = ("00307", "Người dùng không phải là quản trị viên nhóm")
    TASK_FOOD_NOT_FOUND = ("00308", "Không tìm thấy nhiệm vụ với tên đã cung cấp")
    FOOD_ALREADY_IN_SHOPPING_LIST = (
        "00309",
        "Thực phẩm này đã tồn tại trong danh sách mua hàng hiện tại",
    )
    UPDATE_TASK_SUCCESS = ("00312", "Cập nhật nhiệm vụ thành công")

    # Meal Plan Management (00313-00348)
    MISSING_REQUIRED_FIELDS_313 = (
        "00313",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    INVALID_FOOD_NAME_314 = ("00314", "Vui lòng cung cấp một tên thực phẩm hợp lệ")
    INVALID_TIMESTAMP = ("00315", "Vui lòng cung cấp một dấu thời gian hợp lệ")
    INVALID_MEAL_NAME = (
        "00316",
        "Vui lòng cung cấp một tên hợp lệ cho bữa ăn,sáng, trưa, tối",
    )
    FOOD_NOT_FOUND_317 = ("00317", "Không tìm thấy thực phẩm với tên đã cung cấp")
    USER_NOT_GROUP_ADMIN_319 = ("00319", "Người dùng không phải là quản trị viên nhóm")
    ADD_MEAL_PLAN_SUCCESS = ("00322", "Thêm kế hoạch bữa ăn thành công")
    MISSING_REQUIRED_FIELDS_323 = (
        "00323",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    INVALID_PLAN_ID = ("00324", "Vui lòng cung cấp một ID kế hoạch hợp lệ")
    PLAN_NOT_FOUND_325 = ("00325", "Không tìm thấy kế hoạch với ID đã cung cấp")
    USER_NOT_GROUP_ADMIN_327 = ("00327", "Người dùng không phải là quản trị viên nhóm")
    DELETE_MEAL_PLAN_SUCCESS = (
        "00330",
        "Kế hoạch bữa ăn của bạn đã được xóa thành công",
    )
    MISSING_REQUIRED_FIELDS_331 = (
        "00331",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    MISSING_PLAN_ID_332 = ("00332", "Vui lòng cung cấp một ID kế hoạch!")
    MISSING_UPDATE_PLAN_FIELDS = (
        "00333",
        "Vui lòng cung cấp ít nhất một trong các trường sau, newFoodName, newTimestamp, newName",
    )
    INVALID_NEW_FOOD_NAME_334 = (
        "00334",
        "Vui lòng cung cấp một tên thực phẩm mới hợp lệ!",
    )
    INVALID_NEW_TIMESTAMP = ("00335", "Vui lòng cung cấp một dấu thời gian hợp lệ!")
    INVALID_NEW_MEAL_NAME = (
        "00336",
        "Vui lòng cung cấp một tên hợp lệ, sáng, trưa, tối!",
    )
    PLAN_NOT_FOUND_337 = ("00337", "Không tìm thấy kế hoạch với ID đã cung cấp")
    USER_NOT_GROUP_ADMIN_339 = ("00339", "Người dùng không phải là quản trị viên nhóm")
    NEW_FOOD_NAME_NOT_EXISTS_341 = ("00341", "Tên thực phẩm mới không tồn tại")
    UPDATE_MEAL_PLAN_SUCCESS = ("00344", "Cập nhật kế hoạch bữa ăn thành công")
    USER_NOT_IN_GROUP_345 = ("00345", "Bạn chưa vào nhóm nào")
    GET_LIST_SUCCESS = ("00348", "Lấy danh sách thành công")

    # Recipe Management (00349-00378)
    MISSING_REQUIRED_FIELDS_349 = (
        "00349",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    INVALID_FOOD_NAME_350 = ("00350", "Vui lòng cung cấp một tên thực phẩm hợp lệ")
    INVALID_RECIPE_NAME = ("00351", "Vui lòng cung cấp một tên công thức hợp lệ")
    INVALID_RECIPE_DESCRIPTION = (
        "00352",
        "Vui lòng cung cấp một mô tả công thức hợp lệ",
    )
    INVALID_HTML_CONTENT = ("00353", "Vui lòng cung cấp nội dung HTML công thức hợp lệ")
    FOOD_NOT_FOUND_354 = ("00354", "Không tìm thấy thực phẩm với tên đã cung cấp")
    ADD_RECIPE_SUCCESS = ("00357", "Thêm công thức nấu ăn thành công")
    MISSING_REQUIRED_FIELDS_358 = (
        "00358",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    INVALID_RECIPE_ID = ("00359", "Vui lòng cung cấp một ID công thức!")
    MISSING_UPDATE_RECIPE_FIELDS = (
        "00360",
        "Vui lòng cung cấp ít nhất một trong các trường sau, newFoodName, newDescription, newHtmlContent,newName",
    )
    INVALID_NEW_FOOD_NAME_361 = (
        "00361",
        "Vui lòng cung cấp một tên thực phẩm mới hợp lệ!",
    )
    INVALID_NEW_DESCRIPTION = ("00362", "Vui lòng cung cấp một mô tả mới hợp lệ!")
    INVALID_NEW_HTML_CONTENT = ("00363", "Vui lòng cung cấp nội dung HTML mới hợp lệ!")
    INVALID_NEW_RECIPE_NAME = (
        "00364",
        "Vui lòng cung cấp một tên công thức mới hợp lệ!",
    )
    RECIPE_NOT_FOUND_365 = ("00365", "Không tìm thấy công thức với ID đã cung cấp")
    NEW_FOOD_NAME_NOT_EXISTS_367 = ("00367", "Tên thực phẩm mới không tồn tại")
    UPDATE_RECIPE_SUCCESS = ("00370", "Cập nhật công thức nấu ăn thành công")
    MISSING_REQUIRED_FIELDS_371 = (
        "00371",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    INVALID_RECIPE_ID_372 = ("00372", "Vui lòng cung cấp một ID công thức hợp lệ")
    RECIPE_NOT_FOUND_373 = ("00373", "Không tìm thấy công thức với ID đã cung cấp")
    DELETE_RECIPE_SUCCESS = ("00376", "Công thức của bạn đã được xóa thành công")
    GET_RECIPES_SUCCESS = ("00378", "Lấy các công thức thành công")

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message

    @property
    def error_code(self) -> str:
        """Trả về mã lỗi"""
        return self.code

    @property
    def error_message(self) -> str:
        """Trả về thông báo lỗi"""
        return self.message

    def to_dict(self) -> dict:
        """Chuyển đổi thành dictionary"""
        return {"code": self.code, "message": self.message}

    @classmethod
    def get_by_code(cls, code: str) -> "ErrorCode":
        """Lấy ErrorCode theo mã"""
        for error in cls:
            if error.code == code:
                return error
        raise ValueError(f"Không tìm thấy error code: {code}")

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"

    def __repr__(self) -> str:
        return f"ErrorCode(code='{self.code}', message='{self.message}')"


# Utility functions
def get_error_response(error_code: ResponseCode, data=None) -> dict:
    """
    Tạo response chuẩn cho API

    Args:
        error_code: ErrorCode enum
        data: Dữ liệu bổ sung (optional)

    Returns:
        dict: Response chuẩn
    """
    response = {
        "code": error_code.code,
        "message": error_code.message,
        "success": error_code.code
        in [
            "00035",
            "00047",
            "00048",
            "00050",
            "00058",
            "00065",
            "00068",
            "00076",
            "00086",
            "00089",
            "00092",
            "00095",
            "00098",
            "00102",
            "00106",
            "00109",
            "00110",
            "00116",
            "00122",
            "00128",
            "00129",
            "00135",
            "00141",
            "00146",
            "00160",
            "00178",
            "00184",
            "00188",
            "00202",
            "00216",
            "00224",
            "00228",
            "00237",
            "00249",
            "00266",
            "00275",
            "00287",
            "00292",
            "00299",
            "00312",
            "00322",
            "00330",
            "00344",
            "00348",
            "00357",
            "00370",
            "00376",
            "00378",
        ],
    }

    if data is not None:
        response["data"] = data

    return response


def is_success_code(code: str) -> bool:
    """
    Kiểm tra xem mã có phải là mã thành công không

    Args:
        code: Mã lỗi cần kiểm tra

    Returns:
        bool: True nếu là mã thành công
    """
    success_codes = [
        "00035",
        "00047",
        "00048",
        "00050",
        "00058",
        "00065",
        "00068",
        "00076",
        "00086",
        "00089",
        "00092",
        "00095",
        "00098",
        "00102",
        "00106",
        "00109",
        "00110",
        "00116",
        "00122",
        "00128",
        "00129",
        "00135",
        "00141",
        "00146",
        "00160",
        "00178",
        "00184",
        "00188",
        "00202",
        "00216",
        "00224",
        "00228",
        "00237",
        "00249",
        "00266",
        "00275",
        "00287",
        "00292",
        "00299",
        "00312",
        "00322",
        "00330",
        "00344",
        "00348",
        "00357",
        "00370",
        "00376",
        "00378",
    ]
    return code in success_codes
