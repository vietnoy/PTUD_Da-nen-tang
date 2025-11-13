from enum import Enum
from typing import Tuple

# Định nghĩa kiểu dữ liệu cho giá trị của Enum: (mã_code: str, thông_báo: str)
ResultCodeValue = Tuple[str, str]


class ResultCode(Enum):
    """
    Enum chứa các mã kết quả (ResultCode) và thông báo Tiếng Việt tương ứng.
    Giá trị của mỗi thành viên là một tuple (mã code, thông báo chi tiết).
    """

    # --- Mã Thành công (SUCCESS CODES) ---

    SUCCESS = ("00098", "Thành công")
    SUCCESS_REGISTERED = ("00035", "Bạn đã đăng ký thành công.")
    SUCCESS_LOGGED_IN = ("00047", "Bạn đã đăng nhập thành công.")
    SUCCESS_LOGGED_OUT = ("00050", "Đăng xuất thành công.")
    SUCCESS_CODE_SENT = ("00048", "Mã đã được gửi đến email của bạn thành công.")
    SUCCESS_EMAIL_VERIFIED = (
        "00058",
        "Địa chỉ email của bạn đã được xác minh thành công.",
    )
    SUCCESS_TOKEN_REFRESHED = ("00065", "Token đã được làm mới thành công.")
    SUCCESS_PASSWORD_CREATED = ("00068", "Mật khẩu mới đã được tạo thành công.")
    SUCCESS_PASSWORD_CHANGED = (
        "00076",
        "Mật khẩu của bạn đã được thay đổi thành công.",
    )
    SUCCESS_PROFILE_UPDATED = (
        "00086",
        "Thông tin hồ sơ của bạn đã được thay đổi thành công.",
    )
    SUCCESS_USER_FETCHED = ("00089", "Thông tin người dùng đã được lấy thành công.")
    SUCCESS_ACCOUNT_DELETED = ("00092", "Tài khoản của bạn đã bị xóa thành công.")

    # --- Mã Nhóm (GROUP CODES) ---
    SUCCESS_GROUP_CREATED = ("00095", "Tạo nhóm thành công")
    SUCCESS_USER_ADDED_TO_GROUP = ("00102", "Người dùng thêm vào nhóm thành công")
    SUCCESS_GROUP_DELETED = (
        "00106",
        "Xóa thành công",
    )  # Dùng chung cho xóa nhóm/người dùng
    ERROR_ALREADY_IN_GROUP = (
        "00093",
        "Không thể tạo nhóm, bạn đã thuộc về một nhóm rồi",
    )
    ERROR_USER_ALREADY_IN_GROUP = ("00099", "Người này đã thuộc về một nhóm")
    ERROR_NOT_IN_GROUP = ("00096", "Bạn không thuộc về nhóm nào")
    ERROR_USER_NOT_IN_GROUP = ("00103", "Người này chưa vào nhóm nào")
    ERROR_NOT_ADMIN_DELETE = ("00104", "Bạn không phải admin, không thể xóa")
    ERROR_GROUP_USER_NOT_FOUND = (
        "00099x",
        "Không tồn tại user này",
    )  # Cần chuẩn hóa mã 00099x
    ERROR_MISSING_USERNAME = ("00100", "Thiếu username")
    ERROR_MISSING_USERNAME_DELETE = ("00107", "Thiếu username")

    # --- Mã Đơn vị (UNIT CODES) ---
    SUCCESS_UNITS_FETCHED = ("00110", "Lấy các unit thành công")
    SUCCESS_UNIT_CREATED = ("00116", "Tạo đơn vị thành công")
    SUCCESS_UNIT_UPDATED = ("00122", "Sửa đổi đơn vị thành công")
    SUCCESS_UNIT_DELETED = ("00128", "Xóa đơn vị thành công")
    ERROR_MISSING_UNIT_NAME = ("00112", "Thiếu thông tin tên của đơn vị")
    ERROR_UNIT_ALREADY_EXISTS = ("00113", "Đã tồn tại đơn vị có tên này")
    ERROR_MISSING_OLD_NEW_NAME = ("00117", "Thiếu thông tin name cũ, name mới")
    ERROR_OLD_NAME_EQUALS_NEW_NAME = ("00118", "Tên cũ trùng với tên mới")
    ERROR_UNIT_NOT_FOUND = ("00119", "Không tìm thấy đơn vị với tên cung cấp")
    ERROR_MISSING_UNIT_NAME_DELETE = ("00123", "Thiếu thông tin tên của đơn vị")
    ERROR_UNIT_NOT_FOUND_DELETE = ("00125", "Không tìm thấy đơn vị với tên cung cấp")
    SUCCESS_UNIT_FETCHED = ("00111", "Lấy đơn vị thành công")
    # --- Mã Danh mục (CATEGORY CODES) ---
    SUCCESS_CATEGORIES_FETCHED = ("00129", "Lấy các category thành công")
    SUCCESS_CATEGORY_CREATED = ("00135", "Tạo category thành công")
    SUCCESS_CATEGORY_UPDATED = ("00141", "Sửa đổi category thành công")
    SUCCESS_CATEGORY_DELETED = ("00146", "Xóa category thành công")
    ERROR_MISSING_CATEGORY_NAME = ("00131", "Thiếu thông tin tên của category")
    ERROR_CATEGORY_ALREADY_EXISTS = ("00132", "Đã tồn tại category có tên này")
    ERROR_MISSING_OLD_NEW_CATEGORY_NAME = ("00136", "Thiếu thông tin name cũ, name mới")
    ERROR_OLD_CAT_NAME_EQUALS_NEW_CAT_NAME = ("00137", "Tên cũ trùng với tên mới")
    ERROR_CATEGORY_NOT_FOUND = ("00138", "Không tìm thấy category với tên cung cấp")
    ERROR_NEW_CATEGORY_NAME_EXISTS = ("00138x", "Tên mới đã tồn tại")
    ERROR_CATEGORY_NOT_FOUND_DELETE = (
        "00143",
        "Không tìm thấy category với tên cung cấp",
    )
    ERROR_MISSING_CATEGORY_NAME_DELETE = ("00142", "Thiếu thông tin tên của category")

    # --- Mã Lỗi Chung & Server (GENERAL / SERVER CODES) ---
    ERROR_MISSING_FIELDS_SEND_CODE = (
        "00005",
        "Vui lòng cung cấp đầy đủ thông tin để gửi mã.",
    )
    ERROR_ACCESS_DENIED_NO_TOKEN = (
        "00006",
        "Truy cập bị từ chối. Không có token được cung cấp.",
    )
    ERROR_INVALID_USER_ID = ("00007", "ID người dùng không hợp lệ.")
    ERROR_INTERNAL_SERVER = ("00008", "Đã xảy ra lỗi máy chủ nội bộ, vui lòng thử lại.")
    ERROR_USER_NOT_FOUND_VERIFY = (
        "00009",
        "Không thể tìm thấy người dùng đã xác minh với mã và ID được cung cấp. Hãy đảm bảo rằng tài khoản đã được xác minh và kích hoạt.",
    )
    ERROR_SESSION_EXPIRED = (
        "00011",
        "Phiên của bạn đã hết hạn, vui lòng đăng nhập lại.",
    )
    ERROR_INVALID_TOKEN = ("00012", "Token không hợp lệ. Token có thể đã hết hạn.")
    ERROR_ACCESS_DENIED = ("00017", "Truy cập bị từ chối. Bạn không có quyền truy cập.")
    ERROR_ACCESS_DENIED_00019 = (
        "00019",
        "Truy cập bị từ chối. Bạn không có quyền truy cập.",
    )
    ERROR_ACCESS_DENIED_00021 = (
        "00021",
        "Truy cập bị từ chối. Bạn không có quyền truy cập.",
    )
    ERROR_MISSING_ID_IN_PARAM = (
        "00022",
        "Không có ID được cung cấp trong tham số. Vui lòng nhập một ID.",
    )
    ERROR_INVALID_OBJECT_ID = (
        "00023",
        "ID được cung cấp không phải là một đối tượng ID hợp lệ.",
    )
    ERROR_TOO_MANY_REQUESTS = ("00024", "Quá nhiều yêu cầu.")
    ERROR_SERVER_00114 = ("00114", "server error")
    ERROR_SERVER_00115 = ("00115", "server error")
    ERROR_SERVER_00120 = ("00120", "server error")
    ERROR_SERVER_00121 = ("00121", "server error")
    ERROR_SERVER_00126 = ("00126", "server error")
    ERROR_SERVER_00127 = ("00127", "server error")
    ERROR_SERVER_00133 = ("00133", "server error")
    ERROR_SERVER_00134 = ("00134", "server error")
    ERROR_SERVER_00139 = ("00139", "server error")
    ERROR_SERVER_00140 = ("00140", "server error")
    ERROR_SERVER_00144 = ("00144", "server error")
    ERROR_SERVER_00145 = ("00145", "server error")

    # --- Mã Lỗi Xác thực/Đăng ký (AUTH/VALIDATION CODES) ---
    ERROR_MISSING_REQUIRED_FIELDS = (
        "00025",
        "Vui lòng cung cấp tất cả các trường bắt buộc!",
    )
    ERROR_INVALID_EMAIL_FORMAT = (
        "00026",
        "Vui lòng cung cấp một địa chỉ email hợp lệ!",
    )
    ERROR_PASSWORD_LENGTH = (
        "00027",
        "Vui lòng cung cấp mật khẩu dài hơn 6 ký tự và ngắn hơn 20 ký tự.",
    )
    ERROR_NAME_LENGTH = (
        "00028",
        "Vui lòng cung cấp một tên dài hơn 3 ký tự và ngắn hơn 30 ký tự.",
    )
    ERROR_INVALID_EMAIL_00029 = ("00029", "Vui lòng cung cấp một địa chỉ email hợp lệ!")
    ERROR_EMAIL_ALREADY_EXISTS = (
        "00032",
        "Một tài khoản với địa chỉ email này đã tồn tại.",
    )
    ERROR_EMAIL_NOT_FOUND_00036 = (
        "00036",
        "Không tìm thấy tài khoản với địa chỉ email này.",
    )
    ERROR_MISSING_REQUIRED_FIELDS_LOGIN = (
        "00038",
        "Vui lòng cung cấp tất cả các trường bắt buộc!",
    )
    ERROR_INVALID_EMAIL_FORMAT_LOGIN = (
        "00039",
        "Vui lòng cung cấp một địa chỉ email hợp lệ!",
    )
    ERROR_PASSWORD_LENGTH_LOGIN = (
        "00040",
        "Vui lòng cung cấp mật khẩu dài hơn 6 ký tự và ngắn hơn 20 ký tự.",
    )
    ERROR_EMAIL_NOT_FOUND_00042 = (
        "00042",
        "Không tìm thấy tài khoản với địa chỉ email này.",
    )
    ERROR_EMAIL_NOT_ACTIVATED = (
        "00043",
        "Email của bạn chưa được kích hoạt, vui lòng đăng ký trước.",
    )
    ERROR_EMAIL_NOT_VERIFIED = (
        "00044",
        "Email của bạn chưa được xác minh, vui lòng xác minh email của bạn.",
    )
    ERROR_INVALID_CREDENTIALS = (
        "00045",
        "Bạn đã nhập một email hoặc mật khẩu không hợp lệ.",
    )
    ERROR_USER_NOT_FOUND_00052 = ("00052", "Không thể tìm thấy người dùng.")
    ERROR_MISSING_VERIFICATION_CODE = ("00053", "Vui lòng gửi một mã xác nhận.")
    ERROR_CODE_MISMATCH = (
        "00054",
        "Mã bạn nhập không khớp với mã chúng tôi đã gửi đến email của bạn. Vui lòng kiểm tra lại.",
    )
    ERROR_INVALID_TOKEN_00055 = (
        "00055",
        "Token không hợp lệ. Token có thể đã hết hạn.",
    )

    # --- Mã Lỗi Token Refresh (TOKEN REFRESH CODES) ---
    ERROR_MISSING_REFRESH_TOKEN = ("00059", "Vui lòng cung cấp token làm mới.")
    ERROR_TOKEN_USER_MISMATCH = (
        "00061",
        "Token được cung cấp không khớp với người dùng, vui lòng đăng nhập.",
    )
    ERROR_TOKEN_EXPIRED = ("00062", "Token đã hết hạn, vui lòng đăng nhập.")
    ERROR_TOKEN_VERIFICATION_FAILED = (
        "00063",
        "Không thể xác minh token, vui lòng đăng nhập.",
    )

    # --- Mã Lỗi Thay đổi Mật khẩu (PASSWORD CHANGE CODES) ---
    ERROR_PASSWORD_LENGTH_CHANGE = (
        "00066",
        "Vui lòng cung cấp một mật khẩu dài hơn 6 và ngắn hơn 20 ký tự.",
    )
    ERROR_MISSING_OLD_NEW_PASSWORDS = (
        "00069",
        "Vui lòng cung cấp mật khẩu cũ và mới dài hơn 6 ký tự và ngắn hơn 20 ký tự.",
    )
    ERROR_OLD_PASSWORD_MISMATCH = (
        "00072",
        "Mật khẩu cũ của bạn không khớp với mật khẩu bạn nhập, vui lòng nhập mật khẩu đúng.",
    )
    ERROR_NEW_PASSWORD_SAME_AS_OLD = (
        "00073",
        "Mật khẩu mới của bạn không nên giống với mật khẩu cũ, vui lòng thử một mật khẩu khác.",
    )

    # --- Mã Lỗi Cập nhật Hồ sơ (PROFILE UPDATE CODES) ---
    ERROR_NAME_LENGTH_UPDATE = (
        "00077",
        "Vui lòng cung cấp một tên dài hơn 3 ký tự và ngắn hơn 30 ký tự.",
    )
    ERROR_INVALID_GENDER = (
        "00078",
        "Các tùy chọn giới tính hợp lệ, female-male-other, vui lòng cung cấp một trong số chúng.",
    )
    ERROR_INVALID_LANGUAGE = (
        "00079",
        "Các tùy chọn ngôn ngữ hợp lệ, tr-en, vui lòng cung cấp một trong số chúng.",
    )
    ERROR_INVALID_BIRTHDATE = ("00080", "Vui lòng cung cấp một ngày sinh hợp lệ.")
    ERROR_USERNAME_LENGTH = (
        "00081",
        "Vui lòng cung cấp một tên người dùng dài hơn 3 ký tự và ngắn hơn 15 ký tự.",
    )
    ERROR_USERNAME_ALREADY_EXISTS = (
        "00084",
        "Đã có một người dùng với tên người dùng này, vui lòng nhập tên khác.",
    )

    # --- Mã Lỗi Thực phẩm (FOOD/FRIDGE CODES) ---
    ERROR_FOOD_MISSING_REQUIRED_FIELDS = (
        "00147",
        "Vui lòng cung cấp tất cả các trường bắt buộc!",
    )
    ERROR_FOOD_INVALID_NAME = ("00148", "Vui lòng cung cấp tên của thực phẩm hợp lệ!")
    ERROR_FOOD_MISSING_CATEGORY_NAME = (
        "00149",
        "Vui lòng cung cấp tên của category của thực phẩm",
    )
    ERROR_FOOD_MISSING_UNIT_NAME = (
        "00150",
        "Vui lòng cung cấp tên đơn vị đo của thực phẩm",
    )
    ERROR_FOOD_ALREADY_EXISTS = ("00151", "Đã tồn tại thức ăn với tên này")
    ERROR_FOOD_UNIT_NOT_FOUND = ("00153", "Không tìm thấy đơn vị với tên cung cấp")
    ERROR_FOOD_CATEGORY_NOT_FOUND = (
        "00155",
        "Không tìm thấy category với tên cung cấp",
    )
    ERROR_FOOD_NOT_IN_GROUP = ("00156x", "Hãy vào nhóm trước để tạo thực phẩm")
    ERROR_FOOD_UPLOAD_FAILED = ("00158", "đăng tải ảnh thất bại")
    SUCCESS_FOOD_CREATED = ("00160", "Tạo thực phẩm thành công")

    # Mã lỗi cập nhật thực phẩm
    ERROR_FOOD_UPDATE_MISSING_FIELDS = (
        "00161",
        "Vui lòng cung cấp tất cả các trường bắt buộc!",
    )
    ERROR_FOOD_UPDATE_INVALID_NAME = (
        "00162",
        "Vui lòng cung cấp tên thực phẩm hợp lệ!",
    )
    ERROR_FOOD_UPDATE_MISSING_ANY_FIELD = (
        "00163",
        "Vui lòng cung cấp ít nhất một trong các trường sau, newName, newCategory, newUnit",
    )
    ERROR_FOOD_UPDATE_INVALID_NEW_CATEGORY = (
        "00164",
        "Vui lòng cung cấp một danh mục mới hợp lệ cho thực phẩm",
    )
    ERROR_FOOD_UPDATE_INVALID_NEW_UNIT = (
        "00165",
        "Vui lòng cung cấp một đơn vị mới hợp lệ cho thực phẩm",
    )
    ERROR_FOOD_UPDATE_INVALID_NEW_NAME = (
        "00166",
        "Vui lòng cung cấp một tên mới hợp lệ cho thực phẩm",
    )
    ERROR_FOOD_UPDATE_FOOD_NOT_FOUND = (
        "00167",
        "Thực phẩm với tên đã cung cấp không tồn tại",
    )
    ERROR_FOOD_UPDATE_NO_PERMISSION = ("00167x", "Bạn không có quyền chỉnh sửa")
    ERROR_FOOD_UPDATE_UNIT_NOT_FOUND = (
        "00169",
        "Không tìm thấy đơn vị với tên đã cung cấp",
    )
    ERROR_FOOD_UPDATE_CATEGORY_NOT_FOUND = (
        "00171",
        "Không tìm thấy danh mục với tên đã cung cấp",
    )
    ERROR_FOOD_UPDATE_NEW_NAME_ALREADY_EXISTS = (
        "00173",
        "Một thực phẩm với tên này đã tồn tại",
    )
    SUCCESS_FOOD_UPDATED = ("00178", "Thành công")

    # Mã lỗi xóa thực phẩm
    ERROR_FOOD_DELETE_MISSING_NAME = ("00179", "Vui lòng cung cấp tên thực phẩm")
    ERROR_FOOD_DELETE_FOOD_NOT_FOUND = (
        "00180",
        "Không tìm thấy thực phẩm với tên đã cung cấp",
    )
    ERROR_FOOD_DELETE_NO_PERMISSION = ("00181", "Bạn không có quyền")
    SUCCESS_FOOD_DELETED = ("00184", "Xóa thực phẩm thành công")
    ERROR_FOOD_FETCH_NOT_IN_GROUP = ("00185", "Bạn chưa vào nhóm nào")
    SUCCESS_FOOD_LIST_FETCHED = ("00188", "Lấy danh sách thực phẩm thành công")

    # --- Mã Lỗi Tủ lạnh (FRIDGE ITEM CODES) ---
    ERROR_FRIDGE_MISSING_FOOD_NAME = (
        "00190",
        "Vui lòng cung cấp một tên thực phẩm hợp lệ!",
    )
    ERROR_FRIDGE_INVALID_USE_WITHIN = (
        "00191",
        "Vui lòng cung cấp một giá trị 'sử dụng trong khoảng' hợp lệ!",
    )
    ERROR_FRIDGE_INVALID_QUANTITY = ("00192", "Vui lòng cung cấp một số lượng hợp lệ!")
    ERROR_FRIDGE_INVALID_NOTE_FORMAT = ("00193", "Định dạng ghi chú không hợp lệ!")
    ERROR_FRIDGE_FOOD_NOT_EXIST = ("00194", "Thực phẩm không tồn tại.")
    ERROR_FRIDGE_USER_NO_GROUP = (
        "00196",
        "Người dùng không có quyền do không thuộc nhóm.",
    )
    ERROR_FRIDGE_ITEM_NOT_ADMIN = (
        "00198",
        "Thực phẩm không thuộc quyền quản trị của nhóm.",
    )
    ERROR_FRIDGE_ITEM_ALREADY_EXISTS = (
        "00199",
        "Mục trong tủ lạnh cho thực phẩm đã tồn tại.",
    )
    SUCCESS_FRIDGE_ITEM_CREATED = ("00202", "Mục trong tủ lạnh được tạo thành công.")

    # Mã lỗi cập nhật mục tủ lạnh
    ERROR_FRIDGE_UPDATE_MISSING_REQUIRED = (
        "00203",
        "Vui cung cấp tất cả các trường cần thiết",
    )
    ERROR_FRIDGE_UPDATE_MISSING_ID = ("00204", "Vui lòng cung cấp id của item tủ lạnh")
    ERROR_FRIDGE_UPDATE_MISSING_ANY_FIELD = (
        "00204x",
        "Vui lòng cung cấp ít nhất một trong các trường sau, newQuantity, newNote, newUseWithin",
    )
    ERROR_FRIDGE_UPDATE_INVALID_USE_WITHIN = (
        "00205",
        "Vui lòng cung cấp một giá trị 'sử dụng trong' hợp lệ!",
    )
    ERROR_FRIDGE_UPDATE_INVALID_QUANTITY = (
        "00206",
        "Vui lòng cung cấp một lượng hợp lệ!",
    )
    ERROR_FRIDGE_UPDATE_INVALID_NEW_NOTE = (
        "00207",
        "Định dạng ghi chú mới không hợp lệ!",
    )
    ERROR_FRIDGE_UPDATE_INVALID_NEW_FOOD_NAME = (
        "00207x",
        "Định dạng tên thức ăn mới không hợp lệ!",
    )
    ERROR_FRIDGE_UPDATE_FOOD_NOT_EXIST = ("00208", "Thực phẩm không tồn tại.")
    ERROR_FRIDGE_UPDATE_USER_NO_GROUP = (
        "00210",
        "Người dùng không thuộc bất kỳ nhóm nào",
    )
    ERROR_FRIDGE_UPDATE_NOT_GROUP_ADMIN = (
        "00212",
        "Tủ lạnh không thuộc quản trị viên nhóm.",
    )
    ERROR_FRIDGE_UPDATE_ITEM_NOT_EXIST = ("00213", "Mục tủ lạnh không tồn tại.")
    ERROR_FRIDGE_UPDATE_NEW_FOOD_NOT_EXIST = (
        "00214x",
        "Tên thực phẩm mới không tồn tại",
    )
    SUCCESS_FRIDGE_ITEM_UPDATED = ("00216", "Cập nhật mục tủ lạnh thành công.")

    # Mã lỗi xóa/lấy mục tủ lạnh
    ERROR_FRIDGE_DELETE_MISSING_NAME = ("00217", "Vui lòng cung cấp tên thực phẩm")
    ERROR_FRIDGE_DELETE_FOOD_NOT_FOUND = (
        "00218",
        "Không tìm thấy thực phẩm với tên đã cung cấp",
    )
    ERROR_FRIDGE_DELETE_NO_PERMISSION = ("00219", "Bạn không có quyền")
    ERROR_FRIDGE_ITEM_NOT_CREATED = (
        "00221",
        "Mục trong tủ lạnh liên kết với thực phẩm này chưa được tạo",
    )
    SUCCESS_FRIDGE_ITEM_DELETED = ("00224", "Xóa mục trong tủ lạnh thành công")
    ERROR_FRIDGE_LIST_USER_NO_GROUP = ("00225", "Bạn chưa vào nhóm nào")
    SUCCESS_FRIDGE_LIST_FETCHED = ("00228", "Lấy danh sách đồ tủ lạnh thành công")
    SUCCESS_FRIDGE_ITEM_FETCHED = ("00237", "Lấy item cụ thể thành công")

    # --- Mã Lỗi Danh sách Mua sắm (SHOPPING LIST CODES) ---

    # Tạo danh sách
    ERROR_SHOPPING_MISSING_REQUIRED = (
        "00238",
        "Vui cung cấp tất cả các trường cần thiết",
    )
    ERROR_SHOPPING_MISSING_NAME = ("00239", "Vui lòng cung cấp tên")
    ERROR_SHOPPING_MISSING_ASSIGN_TO = ("00240", "Vui lòng cung cấp assignToUsername")
    ERROR_SHOPPING_INVALID_NOTE = ("00241", "Định dạng ghi chú không hợp lệ")
    ERROR_SHOPPING_INVALID_DATE = ("00242", "Định dạng ngày không hợp lệ")
    ERROR_SHOPPING_UNAUTHORIZED_00243 = (
        "00243",
        "Truy cập không được ủy quyền. Bạn không có quyền.",
    )
    ERROR_SHOPPING_ASSIGN_USER_NOT_FOUND = (
        "00245",
        "Tên người dùng được gán không tồn tại.",
    )
    ERROR_SHOPPING_UNAUTHORIZED_ASSIGN = (
        "00246",
        "Truy cập không được ủy quyền. Bạn không có quyền gán danh sách mua sắm cho người dùng này.",
    )
    SUCCESS_SHOPPING_LIST_CREATED = (
        "00249",
        "Danh sách mua sắm đã được tạo thành công.",
    )

    # Cập nhật danh sách
    ERROR_SHOPPING_UPDATE_MISSING_REQUIRED = (
        "00250",
        "Vui cung cấp tất cả các trường cần thiết",
    )
    ERROR_SHOPPING_UPDATE_MISSING_ID = ("00251", "Vui lòng cung cấp id danh sách")
    ERROR_SHOPPING_UPDATE_MISSING_ANY_FIELD = (
        "00252",
        "Vui lòng cung cấp ít nhất một trong những trường sau, newName, newAssignToUsername, newNote,newDate",
    )
    ERROR_SHOPPING_UPDATE_INVALID_NEW_NAME = ("00253", "Định dạng tên mới không hợp lệ")
    ERROR_SHOPPING_UPDATE_INVALID_NEW_ASSIGN_USER = (
        "00254",
        "Định dạng tên người được giao mới không hợp lệ",
    )
    ERROR_SHOPPING_UPDATE_INVALID_NEW_NOTE = (
        "00255",
        "Định dạng ghi chú mới không hợp lệ",
    )
    ERROR_SHOPPING_UPDATE_INVALID_NEW_DATE = (
        "00256",
        "Định dạng ngày mới không hợp lệ",
    )
    ERROR_SHOPPING_UPDATE_NOT_GROUP_ADMIN = (
        "00258",
        "Người dùng không phải là quản trị viên nhóm",
    )
    ERROR_SHOPPING_LIST_NOT_FOUND = ("00260", "Không tìm thấy danh sách mua sắm")
    ERROR_SHOPPING_LIST_NOT_ADMIN = (
        "00261",
        "Người dùng không phải là quản trị viên của danh sách mua sắm này",
    )
    ERROR_SHOPPING_LIST_NEW_USER_NOT_EXIST = ("00262", "Người dùng không tồn tại")
    ERROR_SHOPPING_LIST_UNAUTHORIZED_NEW_ASSIGN = (
        "00263",
        "Người dùng không có quyền gán danh sách này cho tên người dùng",
    )
    SUCCESS_SHOPPING_LIST_UPDATED = ("00266", "Cập nhật danh sách mua sắm thành công")

    # Xóa danh sách
    ERROR_SHOPPING_DELETE_MISSING_REQUIRED = ("00267", "Cung cấp các trường cần thiết")
    ERROR_SHOPPING_DELETE_MISSING_ID = ("00268", "Vui lòng cung cấp id danh sách")
    ERROR_SHOPPING_DELETE_NOT_GROUP_ADMIN = (
        "00270",
        "Người dùng không phải là quản trị viên nhóm",
    )
    ERROR_SHOPPING_DELETE_LIST_NOT_FOUND = ("00272", "Không tìm thấy danh sách mua sắm")
    ERROR_SHOPPING_DELETE_NOT_ADMIN = (
        "00273",
        "Người dùng không phải là quản trị viên của danh sách mua sắm này",
    )
    SUCCESS_SHOPPING_LIST_DELETED = ("00275", "Xóa danh sách mua sắm thành công")

    # --- Mã Lỗi Nhiệm vụ (TASK CODES) ---

    # Thêm nhiệm vụ
    ERROR_TASK_ADD_MISSING_REQUIRED = (
        "00276",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    ERROR_TASK_ADD_MISSING_LIST_ID = ("00277", "Vui lòng cung cấp một ID của danh sách")
    ERROR_TASK_ADD_MISSING_TASK_ARRAY = ("00278", "Vui lòng cung cấp một mảng nhiệm vụ")
    ERROR_TASK_ADD_INVALID_TASK_ARRAY = (
        "00279",
        "Vui lòng cung cấp một mảng nhiệm vụ với các trường hợp lệ",
    )
    ERROR_TASK_ADD_NOT_GROUP_ADMIN = (
        "00281",
        "Người dùng không phải là quản trị viên của nhóm",
    )
    ERROR_TASK_ADD_LIST_NOT_FOUND = ("00283", "Không tìm thấy danh sách mua sắm")
    ERROR_TASK_ADD_NOT_ADMIN = (
        "00284",
        "Người dùng không phải là quản trị viên của danh sách mua sắm này",
    )
    ERROR_TASK_ADD_FOOD_NOT_FOUND = (
        "00285",
        "Không tìm thấy một món ăn với tên cung cấp trong mảng",
    )
    ERROR_TASK_ADD_FOOD_ALREADY_EXISTS = (
        "00285x",
        "Loại thức ăn này đã có trong danh sách rồi",
    )
    SUCCESS_TASK_ADDED = ("00287", "Thêm nhiệm vụ thành công")

    # Lấy danh sách nhiệm vụ
    ERROR_TASK_FETCH_USER_NO_GROUP = ("00288", "Người dùng này chưa thuộc nhóm nào")
    SUCCESS_TASK_LIST_FETCHED = ("00292", "Lấy danh sách các shopping list thành công")

    # Xóa nhiệm vụ
    ERROR_TASK_DELETE_MISSING_REQUIRED = (
        "00293",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    ERROR_TASK_DELETE_MISSING_TASK_ID = (
        "00294",
        "Vui lòng cung cấp một ID nhiệm vụ trong trường taskId",
    )
    ERROR_TASK_DELETE_NOT_FOUND = (
        "00296",
        "Không tìm thấy nhiệm vụ với ID đã cung cấp",
    )
    ERROR_TASK_DELETE_NOT_GROUP_ADMIN = (
        "00297",
        "Người dùng không phải là quản trị viên nhóm",
    )
    SUCCESS_TASK_DELETED = ("00299", "Xóa nhiệm vụ thành công")

    # Cập nhật nhiệm vụ
    ERROR_TASK_UPDATE_MISSING_REQUIRED = (
        "00300",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    ERROR_TASK_UPDATE_MISSING_TASK_ID = (
        "00301",
        "Vui lòng cung cấp một ID nhiệm vụ trong trường taskId",
    )
    ERROR_TASK_UPDATE_MISSING_ANY_FIELD = (
        "00302",
        "Vui lòng cung cấp ít nhất một trong các trường sau, newFoodName, newQuantity",
    )
    ERROR_TASK_UPDATE_INVALID_NEW_FOOD = (
        "00303",
        "Vui lòng cung cấp một newFoodName hợp lệ",
    )
    ERROR_TASK_UPDATE_INVALID_NEW_QUANTITY = (
        "00304",
        "Vui lòng cung cấp một newQuantity hợp lệ",
    )
    ERROR_TASK_UPDATE_NOT_FOUND = (
        "00306",
        "Không tìm thấy nhiệm vụ với ID đã cung cấp",
    )
    ERROR_TASK_UPDATE_NOT_GROUP_ADMIN = (
        "00307",
        "Người dùng không phải là quản trị viên nhóm",
    )
    ERROR_TASK_UPDATE_FOOD_NOT_FOUND = (
        "00308",
        "Không tìm thấy nhiệm vụ với tên đã cung cấp",
    )
    ERROR_TASK_UPDATE_FOOD_ALREADY_EXISTS = (
        "00309",
        "Thực phẩm này đã tồn tại trong danh sách mua hàng hiện tại",
    )
    SUCCESS_TASK_UPDATED = ("00312", "Cập nhật nhiệm vụ thành công")

    # --- Mã Lỗi Kế hoạch Bữa ăn (MEAL PLAN CODES) ---

    # Tạo kế hoạch
    ERROR_MEAL_PLAN_MISSING_REQUIRED = (
        "00313",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    ERROR_MEAL_PLAN_INVALID_FOOD_NAME = (
        "00314",
        "Vui lòng cung cấp một tên thực phẩm hợp lệ",
    )
    ERROR_MEAL_PLAN_INVALID_TIMESTAMP = (
        "00315",
        "Vui lòng cung cấp một dấu thời gian hợp lệ",
    )
    ERROR_MEAL_PLAN_INVALID_NAME = (
        "00316",
        "Vui lòng cung cấp một tên hợp lệ cho bữa ăn,sáng, trưa, tối",
    )
    ERROR_MEAL_PLAN_FOOD_NOT_FOUND = (
        "00317",
        "Không tìm thấy thực phẩm với tên đã cung cấp",
    )
    ERROR_MEAL_PLAN_NOT_GROUP_ADMIN = (
        "00319",
        "Người dùng không phải là quản trị viên nhóm",
    )
    SUCCESS_MEAL_PLAN_ADDED = ("00322", "Thêm kế hoạch bữa ăn thành công")

    # Xóa kế hoạch
    ERROR_MEAL_PLAN_DELETE_MISSING_REQUIRED = (
        "00323",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    ERROR_MEAL_PLAN_DELETE_MISSING_ID = (
        "00324",
        "Vui lòng cung cấp một ID kế hoạch hợp lệ",
    )
    ERROR_MEAL_PLAN_DELETE_NOT_FOUND = (
        "00325",
        "Không tìm thấy kế hoạch với ID đã cung cấp",
    )
    ERROR_MEAL_PLAN_DELETE_NOT_GROUP_ADMIN = (
        "00327",
        "Người dùng không phải là quản trị viên nhóm",
    )
    SUCCESS_MEAL_PLAN_DELETED = (
        "00330",
        "Kế hoạch bữa ăn của bạn đã được xóa thành công",
    )

    # Cập nhật kế hoạch
    ERROR_MEAL_PLAN_UPDATE_MISSING_REQUIRED = (
        "00331",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    ERROR_MEAL_PLAN_UPDATE_MISSING_ID = ("00332", "Vui lòng cung cấp một ID kế hoạch!")
    ERROR_MEAL_PLAN_UPDATE_MISSING_ANY_FIELD = (
        "00333",
        "Vui lòng cung cấp ít nhất một trong các trường sau, newFoodName, newTimestamp, newName",
    )
    ERROR_MEAL_PLAN_UPDATE_INVALID_NEW_FOOD = (
        "00334",
        "Vui lòng cung cấp một tên thực phẩm mới hợp lệ!",
    )
    ERROR_MEAL_PLAN_UPDATE_INVALID_NEW_TIMESTAMP = (
        "00335",
        "Vui lòng cung cấp một dấu thời gian hợp lệ!",
    )
    ERROR_MEAL_PLAN_UPDATE_INVALID_NEW_NAME = (
        "00336",
        "Vui lòng cung cấp một tên hợp lệ, sáng, trưa, tối!",
    )
    ERROR_MEAL_PLAN_UPDATE_NOT_FOUND = (
        "00337",
        "Không tìm thấy kế hoạch với ID đã cung cấp",
    )
    ERROR_MEAL_PLAN_UPDATE_NOT_GROUP_ADMIN = (
        "00339",
        "Người dùng không phải là quản trị viên nhóm",
    )
    ERROR_MEAL_PLAN_UPDATE_NEW_FOOD_NOT_EXIST = (
        "00341",
        "Tên thực phẩm mới không tồn tại",
    )
    SUCCESS_MEAL_PLAN_UPDATED = ("00344", "Cập nhật kế hoạch bữa ăn thành công")

    # Lấy danh sách kế hoạch
    ERROR_MEAL_PLAN_FETCH_USER_NO_GROUP = ("00345", "Bạn chưa vào nhóm nào")
    SUCCESS_MEAL_PLAN_LIST_FETCHED = ("00348", "Lấy danh sách thành công")

    # --- Mã Lỗi Công thức (RECIPE CODES) ---

    # Tạo công thức
    ERROR_RECIPE_MISSING_REQUIRED = (
        "00349",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    ERROR_RECIPE_INVALID_FOOD_NAME = (
        "00350",
        "Vui lòng cung cấp một tên thực phẩm hợp lệ",
    )
    ERROR_RECIPE_INVALID_RECIPE_NAME = (
        "00351",
        "Vui lòng cung cấp một tên công thức hợp lệ",
    )
    ERROR_RECIPE_INVALID_DESCRIPTION = (
        "00352",
        "Vui lòng cung cấp một mô tả công thức hợp lệ",
    )
    ERROR_RECIPE_INVALID_HTML = (
        "00353",
        "Vui lòng cung cấp nội dung HTML công thức hợp lệ",
    )
    ERROR_RECIPE_FOOD_NOT_FOUND = (
        "00354",
        "Không tìm thấy thực phẩm với tên đã cung cấp",
    )
    SUCCESS_RECIPE_ADDED = ("00357", "Thêm công thức nấu ăn thành công")

    # Cập nhật công thức
    ERROR_RECIPE_UPDATE_MISSING_REQUIRED = (
        "00358",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    ERROR_RECIPE_UPDATE_MISSING_ID = ("00359", "Vui lòng cung cấp một ID công thức!")
    ERROR_RECIPE_UPDATE_MISSING_ANY_FIELD = (
        "00360",
        "Vui lòng cung cấp ít nhất một trong các trường sau, newFoodName, newDescription, newHtmlContent,newName",
    )
    ERROR_RECIPE_UPDATE_INVALID_NEW_FOOD = (
        "00361",
        "Vui lòng cung cấp một tên thực phẩm mới hợp lệ!",
    )
    ERROR_RECIPE_UPDATE_INVALID_NEW_DESCRIPTION = (
        "00362",
        "Vui lòng cung cấp một mô tả mới hợp lệ!",
    )
    ERROR_RECIPE_UPDATE_INVALID_NEW_HTML = (
        "00363",
        "Vui lòng cung cấp nội dung HTML mới hợp lệ!",
    )
    ERROR_RECIPE_UPDATE_INVALID_NEW_NAME = (
        "00364",
        "Vui lòng cung cấp một tên công thức mới hợp lệ!",
    )
    ERROR_RECIPE_UPDATE_NOT_FOUND = (
        "00365",
        "Không tìm thấy công thức với ID đã cung cấp",
    )
    ERROR_RECIPE_UPDATE_NEW_FOOD_NOT_EXIST = (
        "00367",
        "Tên thực phẩm mới không tồn tại",
    )
    SUCCESS_RECIPE_UPDATED = ("00370", "Cập nhật công thức nấu ăn thành công")

    # Xóa công thức
    ERROR_RECIPE_DELETE_MISSING_REQUIRED = (
        "00371",
        "Vui lòng cung cấp tất cả các trường bắt buộc",
    )
    ERROR_RECIPE_DELETE_MISSING_ID = (
        "00372",
        "Vui lòng cung cấp một ID công thức hợp lệ",
    )
    ERROR_RECIPE_DELETE_NOT_FOUND = (
        "00373",
        "Không tìm thấy công thức với ID đã cung cấp",
    )
    SUCCESS_RECIPE_DELETED = ("00376", "Công thức của bạn đã được xóa thành công")

    # Lấy danh sách công thức
    SUCCESS_RECIPE_LIST_FETCHED = ("00378", "Lấy các công thức thành công")

    # --- Phương thức tiện ích ---

    @property
    def code(self) -> str:
        """Trả về mã code (ví dụ: '00005')."""
        return self.value[0]

    @property
    def message(self) -> str:
        """Trả về thông báo (ví dụ: 'Vui lòng cung cấp đầy đủ thông tin...')."""
        return self.value[1]


# Ví dụ về cách sử dụng (Không nằm trong file chính, chỉ để minh họa)
if __name__ == "__main__":
    # Cách lấy mã code
    print(f"Mã lỗi đăng nhập: {ResultCode.ERROR_INVALID_CREDENTIALS.code}")
    # Output: Mã lỗi đăng nhập: 00045

    # Cách lấy thông báo
    print(f"Thông báo: {ResultCode.ERROR_INVALID_CREDENTIALS.message}")
    # Output: Thông báo: Bạn đã nhập một email hoặc mật khẩu không hợp lệ.

    # Cách lấy toàn bộ giá trị (tuple)
    print(f"Giá trị đầy đủ: {ResultCode.SUCCESS_LOGGED_IN.value}")
    # Output: Giá trị đầy đủ: ('00047', 'Bạn đã đăng nhập thành công.')
