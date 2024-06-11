from django.urls import path
from . import views as tc

app_name = 'tc'
urlpatterns = [
    path('<int:pk>/apply/',tc.ApplyTcView.as_view(),name='apply_tc'),
    path('<int:pk>/edit-application/',tc.ApplyTcView.as_view(),name='edit_tc'),
    path('<int:pk>/cancel-application/',tc.CancelTcView.as_view(),name='cancel_tc'),
    path('pending/',tc.application_all_view,name='all_tc'),
     path('issued/',tc.tcissued_all_view,name='all_issued_tc'),
    path('<int:pk>/', tc.printTCApplication.as_view(), name='application_view'),
    path('printpendingapplications/', tc.printAllPendingApplications.as_view(), name='printpendingapplications'),
    path('issueprinttcpendingapplications/', tc.IssueprintAllPendingApplications.as_view(), name='issueprintpendingapplications'),
    path('<int:pk>/issue/',tc.tcIssue.as_view(),name = 'tc_issue_view'),
    path('<int:pk>/printtc/',tc.printTC.as_view(),name = 'tc_print_view'),
    ]