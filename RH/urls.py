from django.urls import path
from . import views
from .views import (
    liste_rh,
    ajouter_rh,
    modifier_rh,
    supprimer_rh,
    supprimer_offre,
    rh_login_view,
    dashboard_rh,
    rh_logout_view,
    liste_offre,
    candidats_pour_offre,
    export_candidatures,
    changer_statut_candidature,
    home_view,
    telecharger_convocation,
)
from django.urls import path
from .views import rhe_dashboard
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('candidature/<int:candidature_id>/changer-statut/', changer_statut_candidature, name='changer_statut_candidature'),
    path('', home_view, name='home'),
    path('listerh/', liste_rh, name='liste_rh'),
    path('ajouter/', ajouter_rh, name='ajouter_rh'),
    path('modifier/<int:rh_id>/', modifier_rh, name='modifier_rh'),
    path('rh/supprimer/<int:rh_id>/', supprimer_rh, name='supprimer_rh'),
    path('login/', rh_login_view, name='rh_login'),
    path('dashboard/', dashboard_rh, name='dashboard_rh'),
    path('rh/logout/', rh_logout_view, name='rh_logout'),
    path('liste_offre', views.liste_offres, name='liste_offres'),
    path('creer_offre/', views.creer_offre, name='creer_offre'),
    path('modifier_offre/<int:pk>/', views.modifier_offre, name='modifier_offre'),
    path('offre/supprimer/<int:pk>/', supprimer_offre, name='supprimer_offre'),
    path('register_can/', views.candidat_register_view, name='candidat_register'),
    path('login_can/', views.candidat_login_view, name='candidat_login'),
    path('logout_can/', views.candidat_logout_view, name='candidat_logout'),
    path('dashboard_can/', views.candidat_dashboard, name='candidat_dashboard'),  # à créer
    path('dashboarde/', rhe_dashboard, name='rhe_dashboard'),
    path('candidat/offres/', views.liste_offres_candidat, name='liste_offres_candidat'),
    path('candidat/offres/<int:id>/', views.detail_offre, name='detail_offre'),
    path('candidat/postuler/<int:id>/', views.postuler_offre, name='postuler_offre'),
    path('mes-candidatures/', views.mes_candidatures, name='mes_candidatures'),
    path('off/', views.liste_offres, name='listezs_offres'),
    path('offre/<int:offre_id>/candidatures/', views.candidatures_par_offre, name='candidatures_par_offre'),
    path('offres/<int:offre_id>/', views.detail_offrerh, name='detail_offrerh'),
    path('offres_rh/', liste_offre, name='liste_offr'),
    path('offres_rh/<int:offre_id>/candidats/', candidats_pour_offre, name='candidats_par_offre'),
    path('offre/<int:offre_id>/telecharger/', views.telecharger_offre_pdf, name='telecharger_offre_pdf'),
    path('candidature/<int:candidature_id>/modifier/', views.modifier_statut_candidature, name='modifier_statut_candidature'), 
    path('candidature/<int:candidature_id>/', views.detail_candidature, name='detail_candidature'),
    path('offres/<int:offre_id>/export/', export_candidatures, name='export_candidatures'),
    path('modifier-profil/', views.modifier_profil, name='modifier_profil'),
    path('lesoffres/', views.listedesoffres, name='lesoffres'),
    path('lesoffres/<int:offre_id>/postuler/', views.postuleroffre, name='postulerloffre'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('offres_admin/<int:pk>/', views.offre_detail, name='offre_detail'),
    path('telecharger-convocation/<int:candidature_id>/', telecharger_convocation, name='telecharger_convocation'),
]
    

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



