"""Kubernetes命令管理器

管理和验证Kubernetes命令的学习进度，提供命令信息查询、练习题目生成和学习进度报告。
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import random


class CommandCategory(Enum):
    """命令分类枚举
    
    将Kubernetes命令按照功能进行分类，便于学习和管理。
    """
    基础操作 = "basic"        # 基础命令，如创建、查看、删除Pod
    部署管理 = "deployment"   # 部署相关命令，如创建、扩缩容Deployment
    服务发现 = "service"      # 服务相关命令，如创建、查看Service
    配置管理 = "config"        # 配置相关命令，如ConfigMap、Secret
    存储管理 = "storage"       # 存储相关命令，如PV、PVC
    资源管理 = "resource"      # 资源管理命令，如节点管理、资源配额
    故障排查 = "debug"         # 故障排查命令，如日志查看、容器调试
    进阶操作 = "advanced"      # 进阶命令，如补丁更新、版本回滚
    集群管理 = "cluster"       # 集群管理命令，如权限检查、集群信息
    网络管理 = "network"       # 网络相关命令，如网络策略、CNI配置
    安全管理 = "security"      # 安全相关命令，如RBAC、Secrets管理
    工具命令 = "utility"       # 实用工具命令，如命令补全、插件管理


@dataclass
class KubectlCommand:
    """kubectl命令数据类
    
    存储Kubernetes命令的详细信息，包括名称、分类、描述、语法、示例等。
    
    Attributes:
        name: 命令全名，如"kubectl get pods"
        category: 命令分类
        description: 命令的中文描述
        syntax: 命令的语法格式
        example: 命令的使用示例
        kubernetes_concept: 命令对应的Kubernetes概念
        related_commands: 相关命令列表
        difficulty: 命令难度（1-5）
    """
    name: str
    category: CommandCategory
    description: str
    syntax: str
    example: str
    kubernetes_concept: str
    related_commands: Optional[List[str]] = None
    difficulty: int = 1
    
    def __post_init__(self) -> None:
        """初始化后处理
        
        确保相关命令列表和难度值有效。
        """
        if self.related_commands is None:
            self.related_commands = []
        
        # 确保难度值在1-5之间
        self.difficulty = max(1, min(5, self.difficulty))


class KubernetesCommandManager:
    """Kubernetes命令管理器
    
    管理所有Kubernetes命令的信息，提供命令查询、验证、练习和进度跟踪功能。
    
    Attributes:
        commands: 命令字典，键为命令全名，值为KubectlCommand对象
        command_progress: 命令学习进度，键为命令全名，值为掌握程度（0.0-1.0）
    """
    
    def __init__(self) -> None:
        """初始化命令管理器"""
        self.commands: Dict[str, KubectlCommand] = self._initialize_commands()
        self.command_progress: Dict[str, float] = {}
    
    def _initialize_commands(self) -> Dict[str, KubectlCommand]:
        """初始化所有命令
        
        创建并返回包含所有Kubernetes命令的字典。
        
        Returns:
            Dict[str, KubectlCommand]: 命令字典
        """
        return {
            # 基础操作（难度1）
            "kubectl run": KubectlCommand(
                name="kubectl run",
                category=CommandCategory.基础操作,
                description="创建并运行一个Pod",
                syntax="kubectl run NAME --image=IMAGE",
                example="kubectl run nginx --image=nginx",
                kubernetes_concept="Pod",
                related_commands=["kubectl get pods", "kubectl delete pod"],
                difficulty=1
            ),
            "kubectl get pods": KubectlCommand(
                name="kubectl get pods",
                category=CommandCategory.基础操作,
                description="列出所有Pod",
                syntax="kubectl get pods [OPTIONS]",
                example="kubectl get pods -o wide",
                kubernetes_concept="Pod列表",
                related_commands=["kubectl describe pod"],
                difficulty=1
            ),
            "kubectl describe pod": KubectlCommand(
                name="kubectl describe pod",
                category=CommandCategory.基础操作,
                description="显示Pod的详细信息",
                syntax="kubectl describe pod NAME",
                example="kubectl describe pod nginx-7d9c9c8d8-abcde",
                kubernetes_concept="Pod详情",
                related_commands=["kubectl get pods"],
                difficulty=1
            ),
            "kubectl delete pod": KubectlCommand(
                name="kubectl delete pod",
                category=CommandCategory.基础操作,
                description="删除Pod",
                syntax="kubectl delete pod NAME [OPTIONS]",
                example="kubectl delete pod nginx",
                kubernetes_concept="Pod删除",
                related_commands=["kubectl get pods"],
                difficulty=1
            ),
            "kubectl get all": KubectlCommand(
                name="kubectl get all",
                category=CommandCategory.基础操作,
                description="列出所有资源",
                syntax="kubectl get all [OPTIONS]",
                example="kubectl get all -n default",
                kubernetes_concept="资源列表",
                related_commands=["kubectl get pods", "kubectl get services"],
                difficulty=1
            ),
            "kubectl delete all": KubectlCommand(
                name="kubectl delete all",
                category=CommandCategory.基础操作,
                description="删除所有资源",
                syntax="kubectl delete all NAME [OPTIONS]",
                example="kubectl delete all --all",
                kubernetes_concept="资源删除",
                related_commands=["kubectl delete pod", "kubectl delete service"],
                difficulty=2
            ),
            
            # 部署管理（难度2）
            "kubectl create deployment": KubectlCommand(
                name="kubectl create deployment",
                category=CommandCategory.部署管理,
                description="创建一个Deployment",
                syntax="kubectl create deployment NAME --image=IMAGE",
                example="kubectl create deployment web --image=nginx",
                kubernetes_concept="Deployment",
                related_commands=["kubectl get deployments", "kubectl scale"],
                difficulty=2
            ),
            "kubectl scale": KubectlCommand(
                name="kubectl scale",
                category=CommandCategory.部署管理,
                description="扩缩容Deployment的副本数",
                syntax="kubectl scale deployment NAME --replicas=NUM",
                example="kubectl scale deployment web --replicas=3",
                kubernetes_concept="副本管理",
                related_commands=["kubectl get deployments"],
                difficulty=2
            ),
            "kubectl get deployments": KubectlCommand(
                name="kubectl get deployments",
                category=CommandCategory.部署管理,
                description="列出所有Deployment",
                syntax="kubectl get deployments [OPTIONS]",
                example="kubectl get deployments -o wide",
                kubernetes_concept="Deployment列表",
                related_commands=["kubectl describe deployment"],
                difficulty=2
            ),
            "kubectl rollout status": KubectlCommand(
                name="kubectl rollout status",
                category=CommandCategory.部署管理,
                description="查看Deployment的滚动更新状态",
                syntax="kubectl rollout status deployment NAME",
                example="kubectl rollout status deployment web",
                kubernetes_concept="滚动更新",
                related_commands=["kubectl rollout undo"],
                difficulty=2
            ),
            "kubectl describe deployment": KubectlCommand(
                name="kubectl describe deployment",
                category=CommandCategory.部署管理,
                description="显示Deployment的详细信息",
                syntax="kubectl describe deployment NAME",
                example="kubectl describe deployment web",
                kubernetes_concept="Deployment详情",
                related_commands=["kubectl get deployments"],
                difficulty=2
            ),
            "kubectl delete deployment": KubectlCommand(
                name="kubectl delete deployment",
                category=CommandCategory.部署管理,
                description="删除Deployment",
                syntax="kubectl delete deployment NAME",
                example="kubectl delete deployment web",
                kubernetes_concept="Deployment删除",
                related_commands=["kubectl get deployments"],
                difficulty=2
            ),
            
            # 服务发现（难度2）
            "kubectl expose": KubectlCommand(
                name="kubectl expose",
                category=CommandCategory.服务发现,
                description="为Pod或Deployment创建Service",
                syntax="kubectl expose deployment NAME --port=PORT --type=TYPE",
                example="kubectl expose deployment web --port=80 --type=NodePort",
                kubernetes_concept="Service",
                related_commands=["kubectl get services"],
                difficulty=2
            ),
            "kubectl get services": KubectlCommand(
                name="kubectl get services",
                category=CommandCategory.服务发现,
                description="列出所有Service",
                syntax="kubectl get services [OPTIONS]",
                example="kubectl get svc",
                kubernetes_concept="Service列表",
                related_commands=["kubectl describe service"],
                difficulty=2
            ),
            "kubectl describe service": KubectlCommand(
                name="kubectl describe service",
                category=CommandCategory.服务发现,
                description="显示Service的详细信息",
                syntax="kubectl describe service NAME",
                example="kubectl describe service web",
                kubernetes_concept="Service详情",
                related_commands=["kubectl get services"],
                difficulty=2
            ),
            "kubectl delete service": KubectlCommand(
                name="kubectl delete service",
                category=CommandCategory.服务发现,
                description="删除Service",
                syntax="kubectl delete service NAME",
                example="kubectl delete service web",
                kubernetes_concept="Service删除",
                related_commands=["kubectl get services"],
                difficulty=2
            ),
            "kubectl get endpoints": KubectlCommand(
                name="kubectl get endpoints",
                category=CommandCategory.服务发现,
                description="列出所有Endpoints",
                syntax="kubectl get endpoints [OPTIONS]",
                example="kubectl get endpoints",
                kubernetes_concept="Endpoints",
                related_commands=["kubectl get services"],
                difficulty=3
            ),
            
            # 配置管理（难度3）
            "kubectl create configmap": KubectlCommand(
                name="kubectl create configmap",
                category=CommandCategory.配置管理,
                description="创建ConfigMap",
                syntax="kubectl create configmap NAME --from-literal=key=value",
                example="kubectl create configmap app-config --from-literal=DB_HOST=localhost",
                kubernetes_concept="ConfigMap",
                related_commands=["kubectl get configmaps"],
                difficulty=3
            ),
            "kubectl create secret": KubectlCommand(
                name="kubectl create secret",
                category=CommandCategory.配置管理,
                description="创建Secret",
                syntax="kubectl create secret generic NAME --from-literal=key=value",
                example="kubectl create secret generic db-secret --from-literal=password=secret",
                kubernetes_concept="Secret",
                related_commands=["kubectl get secrets"],
                difficulty=3
            ),
            "kubectl get configmaps": KubectlCommand(
                name="kubectl get configmaps",
                category=CommandCategory.配置管理,
                description="列出所有ConfigMap",
                syntax="kubectl get configmaps [OPTIONS]",
                example="kubectl get configmaps",
                kubernetes_concept="ConfigMap列表",
                related_commands=["kubectl describe configmap"],
                difficulty=2
            ),
            "kubectl get secrets": KubectlCommand(
                name="kubectl get secrets",
                category=CommandCategory.配置管理,
                description="列出所有Secret",
                syntax="kubectl get secrets [OPTIONS]",
                example="kubectl get secrets",
                kubernetes_concept="Secret列表",
                related_commands=["kubectl describe secret"],
                difficulty=2
            ),
            "kubectl describe configmap": KubectlCommand(
                name="kubectl describe configmap",
                category=CommandCategory.配置管理,
                description="显示ConfigMap的详细信息",
                syntax="kubectl describe configmap NAME",
                example="kubectl describe configmap app-config",
                kubernetes_concept="ConfigMap详情",
                related_commands=["kubectl get configmaps"],
                difficulty=2
            ),
            "kubectl delete configmap": KubectlCommand(
                name="kubectl delete configmap",
                category=CommandCategory.配置管理,
                description="删除ConfigMap",
                syntax="kubectl delete configmap NAME",
                example="kubectl delete configmap app-config",
                kubernetes_concept="ConfigMap删除",
                related_commands=["kubectl get configmaps"],
                difficulty=2
            ),
            "kubectl delete secret": KubectlCommand(
                name="kubectl delete secret",
                category=CommandCategory.配置管理,
                description="删除Secret",
                syntax="kubectl delete secret NAME",
                example="kubectl delete secret db-secret",
                kubernetes_concept="Secret删除",
                related_commands=["kubectl get secrets"],
                difficulty=2
            ),
            
            # 存储管理（难度3）
            "kubectl get pv": KubectlCommand(
                name="kubectl get pv",
                category=CommandCategory.存储管理,
                description="列出所有PersistentVolume",
                syntax="kubectl get pv [OPTIONS]",
                example="kubectl get pv",
                kubernetes_concept="PersistentVolume",
                related_commands=["kubectl describe pv"],
                difficulty=3
            ),
            "kubectl get pvc": KubectlCommand(
                name="kubectl get pvc",
                category=CommandCategory.存储管理,
                description="列出所有PersistentVolumeClaim",
                syntax="kubectl get pvc [OPTIONS]",
                example="kubectl get pvc",
                kubernetes_concept="PersistentVolumeClaim",
                related_commands=["kubectl describe pvc"],
                difficulty=3
            ),
            "kubectl apply": KubectlCommand(
                name="kubectl apply",
                category=CommandCategory.存储管理,
                description="从YAML文件创建或更新资源",
                syntax="kubectl apply -f FILENAME",
                example="kubectl apply -f deployment.yaml",
                kubernetes_concept="声明式配置",
                related_commands=["kubectl delete"],
                difficulty=3
            ),
            "kubectl delete pvc": KubectlCommand(
                name="kubectl delete pvc",
                category=CommandCategory.存储管理,
                description="删除PersistentVolumeClaim",
                syntax="kubectl delete pvc NAME",
                example="kubectl delete pvc my-pvc",
                kubernetes_concept="PVC删除",
                related_commands=["kubectl get pvc"],
                difficulty=3
            ),
            "kubectl get storageclasses": KubectlCommand(
                name="kubectl get storageclasses",
                category=CommandCategory.存储管理,
                description="列出所有StorageClass",
                syntax="kubectl get storageclasses [OPTIONS]",
                example="kubectl get sc",
                kubernetes_concept="StorageClass",
                related_commands=["kubectl describe storageclass"],
                difficulty=4
            ),
            "kubectl delete pv": KubectlCommand(
                name="kubectl delete pv",
                category=CommandCategory.存储管理,
                description="删除PersistentVolume",
                syntax="kubectl delete pv NAME",
                example="kubectl delete pv my-pv",
                kubernetes_concept="PV删除",
                related_commands=["kubectl get pv"],
                difficulty=4
            ),
            
            # 资源管理（难度3）
            "kubectl top": KubectlCommand(
                name="kubectl top",
                category=CommandCategory.资源管理,
                description="查看资源使用情况",
                syntax="kubectl top pods [OPTIONS]",
                example="kubectl top pods",
                kubernetes_concept="资源监控",
                related_commands=["kubectl describe"],
                difficulty=3
            ),
            "kubectl top node": KubectlCommand(
                name="kubectl top node",
                category=CommandCategory.资源管理,
                description="查看节点资源使用情况",
                syntax="kubectl top node [OPTIONS]",
                example="kubectl top node worker-1",
                kubernetes_concept="节点资源监控",
                related_commands=["kubectl top"],
                difficulty=3
            ),
            "kubectl describe node": KubectlCommand(
                name="kubectl describe node",
                category=CommandCategory.资源管理,
                description="显示Node的详细信息",
                syntax="kubectl describe node NAME",
                example="kubectl describe node worker-1",
                kubernetes_concept="Node详情",
                related_commands=["kubectl get nodes"],
                difficulty=3
            ),
            "kubectl label node": KubectlCommand(
                name="kubectl label node",
                category=CommandCategory.资源管理,
                description="为Node添加标签",
                syntax="kubectl label node NAME KEY=VALUE",
                example="kubectl label node worker-1 disktype=ssd",
                kubernetes_concept="节点标签",
                related_commands=["kubectl get nodes"],
                difficulty=3
            ),
            "kubectl taint node": KubectlCommand(
                name="kubectl taint node",
                category=CommandCategory.资源管理,
                description="为Node添加污点",
                syntax="kubectl taint node NAME KEY=VALUE:EFFECT",
                example="kubectl taint node master-1 node-role.kubernetes.io/master:NoSchedule",
                kubernetes_concept="节点污点",
                related_commands=["kubectl get nodes"],
                difficulty=4
            ),
            "kubectl untaint node": KubectlCommand(
                name="kubectl untaint node",
                category=CommandCategory.资源管理,
                description="移除Node的污点",
                syntax="kubectl untaint node NAME KEY:EFFECT-",
                example="kubectl untaint node worker-1 dedicated:NoSchedule-",
                kubernetes_concept="节点污点移除",
                related_commands=["kubectl taint node"],
                difficulty=4
            ),
            "kubectl get nodes": KubectlCommand(
                name="kubectl get nodes",
                category=CommandCategory.资源管理,
                description="列出所有Node",
                syntax="kubectl get nodes [OPTIONS]",
                example="kubectl get nodes -o wide",
                kubernetes_concept="Node列表",
                related_commands=["kubectl describe node"],
                difficulty=2
            ),
            "kubectl cordon node": KubectlCommand(
                name="kubectl cordon node",
                category=CommandCategory.资源管理,
                description="标记节点为不可调度",
                syntax="kubectl cordon node NAME",
                example="kubectl cordon node worker-1",
                kubernetes_concept="节点调度",
                related_commands=["kubectl uncordon node"],
                difficulty=3
            ),
            "kubectl uncordon node": KubectlCommand(
                name="kubectl uncordon node",
                category=CommandCategory.资源管理,
                description="标记节点为可调度",
                syntax="kubectl uncordon node NAME",
                example="kubectl uncordon node worker-1",
                kubernetes_concept="节点调度",
                related_commands=["kubectl cordon node"],
                difficulty=3
            ),
            "kubectl drain node": KubectlCommand(
                name="kubectl drain node",
                category=CommandCategory.资源管理,
                description="驱逐节点上的所有Pod",
                syntax="kubectl drain node NAME [OPTIONS]",
                example="kubectl drain node worker-1 --ignore-daemonsets",
                kubernetes_concept="节点维护",
                related_commands=["kubectl cordon node"],
                difficulty=4
            ),
            "kubectl cp": KubectlCommand(
                name="kubectl cp",
                category=CommandCategory.资源管理,
                description="在本地和Pod之间复制文件",
                syntax="kubectl cp LOCAL_PATH POD:REMOTE_PATH",
                example="kubectl cp /local/file.txt my-pod:/remote/path/",
                kubernetes_concept="文件复制",
                related_commands=["kubectl exec"],
                difficulty=3
            ),
            "kubectl logs -f": KubectlCommand(
                name="kubectl logs -f",
                category=CommandCategory.资源管理,
                description="实时查看Pod日志",
                syntax="kubectl logs -f POD [OPTIONS]",
                example="kubectl logs -f web-7d9c9c9d8-abcde",
                kubernetes_concept="实时日志查看",
                related_commands=["kubectl logs"],
                difficulty=3
            ),
            "kubectl annotate": KubectlCommand(
                name="kubectl annotate",
                category=CommandCategory.资源管理,
                description="为资源添加注解",
                syntax="kubectl annotate RESOURCE NAME KEY=VALUE",
                example="kubectl annotate pod web-1 description='production app'",
                kubernetes_concept="资源注解",
                related_commands=["kubectl label"],
                difficulty=4
            ),
            
            # 故障排查（难度4）
            "kubectl logs": KubectlCommand(
                name="kubectl logs",
                category=CommandCategory.故障排查,
                description="查看Pod的日志",
                syntax="kubectl logs POD [OPTIONS]",
                example="kubectl logs web-7d9c9c9d8-abcde --tail=100",
                kubernetes_concept="日志查看",
                related_commands=["kubectl describe"],
                difficulty=3
            ),
            "kubectl exec": KubectlCommand(
                name="kubectl exec",
                category=CommandCategory.故障排查,
                description="在Pod中执行命令",
                syntax="kubectl exec POD -- COMMAND",
                example="kubectl exec -it web-7d9c9c9d8-abcde -- /bin/sh",
                kubernetes_concept="容器调试",
                related_commands=["kubectl logs"],
                difficulty=3
            ),
            "kubectl port-forward": KubectlCommand(
                name="kubectl port-forward",
                category=CommandCategory.故障排查,
                description="本地端口转发到Pod",
                syntax="kubectl port-forward POD LOCAL_PORT:REMOTE_PORT",
                example="kubectl port-forward svc/web 8080:80",
                kubernetes_concept="端口转发",
                related_commands=["kubectl logs"],
                difficulty=3
            ),
            "kubectl events": KubectlCommand(
                name="kubectl events",
                category=CommandCategory.故障排查,
                description="查看集群事件",
                syntax="kubectl events [OPTIONS]",
                example="kubectl events --sort-by='.lastTimestamp'",
                kubernetes_concept="事件监控",
                related_commands=["kubectl describe"],
                difficulty=3
            ),
            "kubectl debug": KubectlCommand(
                name="kubectl debug",
                category=CommandCategory.故障排查,
                description="调试Pod",
                syntax="kubectl debug POD [OPTIONS]",
                example="kubectl debug web-7d9c9c9d8-abcde --image=busybox",
                kubernetes_concept="Pod调试",
                related_commands=["kubectl exec"],
                difficulty=4
            ),
            "kubectl get events": KubectlCommand(
                name="kubectl get events",
                category=CommandCategory.故障排查,
                description="列出所有事件",
                syntax="kubectl get events [OPTIONS]",
                example="kubectl get events --field-selector type=Warning",
                kubernetes_concept="事件查询",
                related_commands=["kubectl describe"],
                difficulty=3
            ),
            
            # 进阶操作（难度4）
            "kubectl patch": KubectlCommand(
                name="kubectl patch",
                category=CommandCategory.进阶操作,
                description="更新资源的字段",
                syntax="kubectl patch TYPE NAME -p PATCH",
                example="kubectl patch deployment web -p '{\"spec\":{\"replicas\":5}}'",
                kubernetes_concept="补丁更新",
                related_commands=["kubectl apply"],
                difficulty=4
            ),
            "kubectl set image": KubectlCommand(
                name="kubectl set image",
                category=CommandCategory.进阶操作,
                description="更新容器镜像",
                syntax="kubectl set image deployment NAME CONTAINER=IMAGE",
                example="kubectl set image deployment web nginx=nginx:1.21",
                kubernetes_concept="镜像更新",
                related_commands=["kubectl rollout"],
                difficulty=4
            ),
            "kubectl rollout undo": KubectlCommand(
                name="kubectl rollout undo",
                category=CommandCategory.进阶操作,
                description="回滚Deployment到上一版本",
                syntax="kubectl rollout undo deployment NAME",
                example="kubectl rollout undo deployment web",
                kubernetes_concept="版本回滚",
                related_commands=["kubectl rollout status"],
                difficulty=4
            ),
            "kubectl rollout history": KubectlCommand(
                name="kubectl rollout history",
                category=CommandCategory.进阶操作,
                description="查看Deployment的版本历史",
                syntax="kubectl rollout history deployment NAME",
                example="kubectl rollout history deployment web",
                kubernetes_concept="版本历史",
                related_commands=["kubectl rollout undo"],
                difficulty=4
            ),
            "kubectl replace": KubectlCommand(
                name="kubectl replace",
                category=CommandCategory.进阶操作,
                description="替换资源",
                syntax="kubectl replace -f FILENAME",
                example="kubectl replace -f deployment.yaml",
                kubernetes_concept="资源替换",
                related_commands=["kubectl apply"],
                difficulty=4
            ),
            "kubectl edit": KubectlCommand(
                name="kubectl edit",
                category=CommandCategory.进阶操作,
                description="编辑资源",
                syntax="kubectl edit TYPE NAME",
                example="kubectl edit deployment web",
                kubernetes_concept="资源编辑",
                related_commands=["kubectl apply"],
                difficulty=4
            ),
            
            # 集群管理（难度5）
            "kubectl auth can-i": KubectlCommand(
                name="kubectl auth can-i",
                category=CommandCategory.集群管理,
                description="检查当前用户的权限",
                syntax="kubectl auth can-i VERB RESOURCE",
                example="kubectl auth can-i create pods",
                kubernetes_concept="权限检查",
                related_commands=["kubectl auth"],
                difficulty=5
            ),
            "kubectl config view": KubectlCommand(
                name="kubectl config view",
                category=CommandCategory.集群管理,
                description="显示kubeconfig配置",
                syntax="kubectl config view",
                example="kubectl config view",
                kubernetes_concept="配置查看",
                related_commands=["kubectl config"],
                difficulty=4
            ),
            "kubectl cluster-info": KubectlCommand(
                name="kubectl cluster-info",
                category=CommandCategory.集群管理,
                description="显示集群信息",
                syntax="kubectl cluster-info",
                example="kubectl cluster-info",
                kubernetes_concept="集群信息",
                related_commands=["kubectl get nodes"],
                difficulty=4
            ),
            "kubectl api-resources": KubectlCommand(
                name="kubectl api-resources",
                category=CommandCategory.集群管理,
                description="列出所有可用的API资源",
                syntax="kubectl api-resources [OPTIONS]",
                example="kubectl api-resources",
                kubernetes_concept="API资源",
                related_commands=["kubectl get"],
                difficulty=4
            ),
            "kubectl completion": KubectlCommand(
                name="kubectl completion",
                category=CommandCategory.工具命令,
                description="生成shell补全脚本",
                syntax="kubectl completion shell",
                example="kubectl completion bash",
                kubernetes_concept="命令补全",
                related_commands=["kubectl"],
                difficulty=2
            ),
            "kubectl version": KubectlCommand(
                name="kubectl version",
                category=CommandCategory.工具命令,
                description="显示kubectl版本信息",
                syntax="kubectl version [OPTIONS]",
                example="kubectl version --short",
                kubernetes_concept="版本信息",
                related_commands=["kubectl"],
                difficulty=1
            ),
            "kubectl plugin list": KubectlCommand(
                name="kubectl plugin list",
                category=CommandCategory.工具命令,
                description="列出所有kubectl插件",
                syntax="kubectl plugin list",
                example="kubectl plugin list",
                kubernetes_concept="插件管理",
                related_commands=["kubectl"],
                difficulty=3
            ),
            
            # 网络管理（难度5）
            "kubectl get networkpolicies": KubectlCommand(
                name="kubectl get networkpolicies",
                category=CommandCategory.网络管理,
                description="列出所有网络策略",
                syntax="kubectl get networkpolicies [OPTIONS]",
                example="kubectl get networkpolicies",
                kubernetes_concept="网络策略",
                related_commands=["kubectl describe networkpolicy"],
                difficulty=5
            ),
            "kubectl describe networkpolicy": KubectlCommand(
                name="kubectl describe networkpolicy",
                category=CommandCategory.网络管理,
                description="显示网络策略的详细信息",
                syntax="kubectl describe networkpolicy NAME",
                example="kubectl describe networkpolicy default-deny",
                kubernetes_concept="网络策略详情",
                related_commands=["kubectl get networkpolicies"],
                difficulty=5
            ),
            "kubectl create networkpolicy": KubectlCommand(
                name="kubectl create networkpolicy",
                category=CommandCategory.网络管理,
                description="创建网络策略",
                syntax="kubectl create networkpolicy NAME --allow --from=SOURCE [OPTIONS]",
                example="kubectl create networkpolicy allow-from-web --allow --from=podSelector:app=web",
                kubernetes_concept="网络策略创建",
                related_commands=["kubectl get networkpolicies"],
                difficulty=5
            ),
            "kubectl delete networkpolicy": KubectlCommand(
                name="kubectl delete networkpolicy",
                category=CommandCategory.网络管理,
                description="删除网络策略",
                syntax="kubectl delete networkpolicy NAME",
                example="kubectl delete networkpolicy default-deny",
                kubernetes_concept="网络策略删除",
                related_commands=["kubectl get networkpolicies"],
                difficulty=5
            ),
            "kubectl get ingress": KubectlCommand(
                name="kubectl get ingress",
                category=CommandCategory.网络管理,
                description="列出所有Ingress资源",
                syntax="kubectl get ingress [OPTIONS]",
                example="kubectl get ingress",
                kubernetes_concept="Ingress资源",
                related_commands=["kubectl describe ingress"],
                difficulty=4
            ),
            "kubectl describe ingress": KubectlCommand(
                name="kubectl describe ingress",
                category=CommandCategory.网络管理,
                description="显示Ingress的详细信息",
                syntax="kubectl describe ingress NAME",
                example="kubectl describe ingress web-ingress",
                kubernetes_concept="Ingress详情",
                related_commands=["kubectl get ingress"],
                difficulty=4
            ),
            "kubectl delete ingress": KubectlCommand(
                name="kubectl delete ingress",
                category=CommandCategory.网络管理,
                description="删除Ingress资源",
                syntax="kubectl delete ingress NAME",
                example="kubectl delete ingress web-ingress",
                kubernetes_concept="Ingress删除",
                related_commands=["kubectl get ingress"],
                difficulty=4
            ),
            
            # 安全管理（难度5）
            "kubectl get roles": KubectlCommand(
                name="kubectl get roles",
                category=CommandCategory.安全管理,
                description="列出所有Role",
                syntax="kubectl get roles [OPTIONS]",
                example="kubectl get roles",
                kubernetes_concept="Role",
                related_commands=["kubectl describe role"],
                difficulty=5
            ),
            "kubectl get rolebindings": KubectlCommand(
                name="kubectl get rolebindings",
                category=CommandCategory.安全管理,
                description="列出所有RoleBinding",
                syntax="kubectl get rolebindings [OPTIONS]",
                example="kubectl get rolebindings",
                kubernetes_concept="RoleBinding",
                related_commands=["kubectl describe rolebinding"],
                difficulty=5
            ),
            "kubectl get clusterroles": KubectlCommand(
                name="kubectl get clusterroles",
                category=CommandCategory.安全管理,
                description="列出所有ClusterRole",
                syntax="kubectl get clusterroles [OPTIONS]",
                example="kubectl get clusterroles",
                kubernetes_concept="ClusterRole",
                related_commands=["kubectl describe clusterrole"],
                difficulty=5
            ),
            "kubectl get clusterrolebindings": KubectlCommand(
                name="kubectl get clusterrolebindings",
                category=CommandCategory.安全管理,
                description="列出所有ClusterRoleBinding",
                syntax="kubectl get clusterrolebindings [OPTIONS]",
                example="kubectl get clusterrolebindings",
                kubernetes_concept="ClusterRoleBinding",
                related_commands=["kubectl describe clusterrolebinding"],
                difficulty=5
            ),
            "kubectl create role": KubectlCommand(
                name="kubectl create role",
                category=CommandCategory.安全管理,
                description="创建Role",
                syntax="kubectl create role NAME --verb=VERB --resource=RESOURCE",
                example="kubectl create role pod-reader --verb=get --resource=pods",
                kubernetes_concept="Role创建",
                related_commands=["kubectl get roles"],
                difficulty=5
            ),
            "kubectl create rolebinding": KubectlCommand(
                name="kubectl create rolebinding",
                category=CommandCategory.安全管理,
                description="创建RoleBinding",
                syntax="kubectl create rolebinding NAME --role=ROLE --user=USER",
                example="kubectl create rolebinding alice-pod-reader --role=pod-reader --user=alice",
                kubernetes_concept="RoleBinding创建",
                related_commands=["kubectl get rolebindings"],
                difficulty=5
            ),
            "kubectl create secret generic": KubectlCommand(
                name="kubectl create secret generic",
                category=CommandCategory.安全管理,
                description="从文件或字面量创建Secret",
                syntax="kubectl create secret generic NAME --from-literal=KEY=VALUE",
                example="kubectl create secret generic db-secret --from-literal=password=secret123",
                kubernetes_concept="Secret创建",
                related_commands=["kubectl get secrets"],
                difficulty=4
            ),
            "kubectl create secret docker-registry": KubectlCommand(
                name="kubectl create secret docker-registry",
                category=CommandCategory.安全管理,
                description="创建Docker Registry认证Secret",
                syntax="kubectl create secret docker-registry NAME --docker-server=SERVER --docker-username=USER --docker-password=PASSWORD",
                example="kubectl create secret docker-registry reg-cred --docker-server=registry.example.com --docker-username=admin --docker-password=pass123",
                kubernetes_concept="镜像仓库认证",
                related_commands=["kubectl get secrets"],
                difficulty=4
            ),
            "kubectl get secrets": KubectlCommand(
                name="kubectl get secrets",
                category=CommandCategory.安全管理,
                description="列出所有Secret",
                syntax="kubectl get secrets [OPTIONS]",
                example="kubectl get secrets -o yaml",
                kubernetes_concept="Secret列表",
                related_commands=["kubectl describe secret"],
                difficulty=4
            ),
            "kubectl describe secret": KubectlCommand(
                name="kubectl describe secret",
                category=CommandCategory.安全管理,
                description="显示Secret的详细信息",
                syntax="kubectl describe secret NAME",
                example="kubectl describe secret db-secret",
                kubernetes_concept="Secret详情",
                related_commands=["kubectl get secrets"],
                difficulty=4
            ),
            "kubectl delete secret": KubectlCommand(
                name="kubectl delete secret",
                category=CommandCategory.安全管理,
                description="删除Secret",
                syntax="kubectl delete secret NAME",
                example="kubectl delete secret old-secret",
                kubernetes_concept="Secret删除",
                related_commands=["kubectl get secrets"],
                difficulty=4
            ),
            "kubectl auth can-i": KubectlCommand(
                name="kubectl auth can-i",
                category=CommandCategory.安全管理,
                description="检查当前用户的权限",
                syntax="kubectl auth can-i VERB RESOURCE [--namespace=NAMESPACE]",
                example="kubectl auth can-i create pods --namespace=default",
                kubernetes_concept="权限检查",
                related_commands=["kubectl auth"],
                difficulty=5
            ),
            "kubectl get serviceaccounts": KubectlCommand(
                name="kubectl get serviceaccounts",
                category=CommandCategory.安全管理,
                description="列出所有ServiceAccount",
                syntax="kubectl get serviceaccounts [OPTIONS]",
                example="kubectl get sa",
                kubernetes_concept="ServiceAccount",
                related_commands=["kubectl describe serviceaccount"],
                difficulty=4
            ),
            "kubectl describe serviceaccount": KubectlCommand(
                name="kubectl describe serviceaccount",
                category=CommandCategory.安全管理,
                description="显示ServiceAccount的详细信息",
                syntax="kubectl describe serviceaccount NAME",
                example="kubectl describe sa default",
                kubernetes_concept="ServiceAccount详情",
                related_commands=["kubectl get serviceaccounts"],
                difficulty=4
            ),
        }
    
    def get_command(self, command_name: str) -> Optional[KubectlCommand]:
        """获取命令信息
        
        根据命令名称获取命令的详细信息。
        
        Args:
            command_name: 命令全名，如"kubectl get pods"
            
        Returns:
            Optional[KubectlCommand]: 命令信息对象，如果不存在则返回None
        """
        if not isinstance(command_name, str):
            raise ValueError("命令名称必须是字符串类型")
        
        return self.commands.get(command_name)
    
    def get_commands_by_category(self, category: CommandCategory) -> List[KubectlCommand]:
        """按分类获取命令
        
        获取指定分类下的所有命令。
        
        Args:
            category: 命令分类
            
        Returns:
            List[KubectlCommand]: 命令列表
        """
        if not isinstance(category, CommandCategory):
            raise ValueError("分类必须是CommandCategory枚举类型")
        
        return [cmd for cmd in self.commands.values() if cmd.category == category]
    
    def get_commands_by_difficulty(self, difficulty: int) -> List[KubectlCommand]:
        """按难度获取命令
        
        获取指定难度级别的所有命令。
        
        Args:
            difficulty: 难度级别（1-5）
            
        Returns:
            List[KubectlCommand]: 命令列表
        """
        if not isinstance(difficulty, int) or difficulty < 1 or difficulty > 5:
            raise ValueError("难度必须是1-5之间的整数")
        
        return [cmd for cmd in self.commands.values() if cmd.difficulty == difficulty]
    
    def get_all_commands(self) -> List[str]:
        """获取所有命令名
        
        返回所有已定义命令的名称列表。
        
        Returns:
            List[str]: 命令名称列表
        """
        return sorted(list(self.commands.keys()))
    
    def get_command_categories(self) -> List[CommandCategory]:
        """获取所有命令分类
        
        返回所有已使用的命令分类列表。
        
        Returns:
            List[CommandCategory]: 命令分类列表
        """
        return sorted(list(set(cmd.category for cmd in self.commands.values())), key=lambda x: x.value)
    
    def validate_command(self, command: str) -> Tuple[bool, Optional[KubectlCommand], str]:
        """验证命令是否正确
        
        检查命令是否已定义，并返回验证结果。
        
        Args:
            command: 要验证的命令
            
        Returns:
            Tuple[bool, Optional[KubectlCommand], str]: 验证结果，包含是否正确、命令信息和消息
        """
        if not isinstance(command, str):
            return False, None, "命令必须是字符串类型"
        
        if command in self.commands:
            cmd = self.commands[command]
            return True, cmd, f"✓ 掌握命令: {command}\n  说明: {cmd.description}"
        
        # 检查是否是大小写错误
        for cmd_name in self.commands:
            if command.lower() == cmd_name.lower():
                return False, None, f"命令格式不正确，请使用完整命令格式: {cmd_name}"
        
        # 检查是否是部分匹配
        partial_matches = [cmd_name for cmd_name in self.commands if command in cmd_name]
        if partial_matches:
            return False, None, f"✗ 命令不完整，可能的命令有: {', '.join(partial_matches)}"
        
        return False, None, "✗ 未知命令，请检查拼写"
    
    def get_practice_question(self, chapter_commands: List[str]) -> Optional[Dict[str, Any]]:
        """生成练习题
        
        根据指定的章节命令列表生成一道练习题。
        
        Args:
            chapter_commands: 章节命令列表
            
        Returns:
            Optional[Dict[str, Any]]: 练习题字典，包含问题、提示、答案等
        """
        if not chapter_commands or not isinstance(chapter_commands, list):
            return None
        
        # 过滤掉无效命令
        valid_commands = [cmd for cmd in chapter_commands if cmd in self.commands]
        if not valid_commands:
            return None
        
        # 从本章命令中随机选择
        target_command = random.choice(valid_commands)
        cmd_info = self.commands.get(target_command)
        
        if not cmd_info:
            return None
        
        return {
            "question": f"如何{cmd_info.description}？",
            "hint": f"使用 {cmd_info.syntax} 格式",
            "answer": target_command,
            "syntax": cmd_info.syntax,
            "example": cmd_info.example,
            "command": target_command,
            "concept": cmd_info.kubernetes_concept,
            "difficulty": cmd_info.difficulty
        }
    
    def get_random_challenge(self, mastered_commands: List[str], difficulty: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """生成随机挑战
        
        生成一个随机的挑战题，可指定难度。
        
        Args:
            mastered_commands: 已掌握的命令列表
            difficulty: 挑战难度（1-5），如果为None则随机
            
        Returns:
            Optional[Dict[str, Any]]: 挑战题字典
        """
        # 选择未掌握的命令
        mastered_set = set(mastered_commands)
        available_commands = [cmd for cmd in self.commands.values() if cmd.name not in mastered_set]
        
        if not available_commands:
            return None
        
        # 根据难度过滤
        if difficulty is not None:
            available_commands = [cmd for cmd in available_commands if cmd.difficulty == difficulty]
            if not available_commands:
                return None
        
        # 随机选择一个命令
        target_cmd = random.choice(available_commands)
        
        return {
            "title": f"挑战: {target_cmd.kubernetes_concept}",
            "description": f"请写出{target_cmd.description}的命令",
            "question": f"如何{target_cmd.description}？",
            "hint": f"语法格式: {target_cmd.syntax}",
            "answer": target_cmd.name,
            "example": target_cmd.example,
            "concept": target_cmd.kubernetes_concept,
            "difficulty": target_cmd.difficulty,
            "related_commands": target_cmd.related_commands
        }
    
    def get_progress_report(self, mastered_commands: List[str]) -> Dict[str, Any]:
        """获取学习进度报告
        
        生成详细的学习进度报告，包括总进度、分类进度等。
        
        Args:
            mastered_commands: 已掌握的命令列表
            
        Returns:
            Dict[str, Any]: 进度报告字典
        """
        if not isinstance(mastered_commands, list):
            mastered_commands = []
        
        total = len(self.commands)
        mastered_set = set(mastered_commands)
        mastered = len([cmd for cmd in mastered_set if cmd in self.commands])
        
        by_category = {}
        for category in self.get_command_categories():
            category_commands = self.get_commands_by_category(category)
            category_total = len(category_commands)
            if category_total == 0:
                continue
                
            category_mastered = len([
                c.name
                for c in category_commands
                if c.name in mastered_set
            ])
            
            by_category[category.value] = {
                "category_name": category.name,
                "total": category_total,
                "mastered": category_mastered,
                "percentage": round(category_mastered / category_total * 100, 1) if category_total > 0 else 0
            }
        
        # 按难度统计
        by_difficulty = {}
        for difficulty in range(1, 6):
            diff_commands = self.get_commands_by_difficulty(difficulty)
            diff_total = len(diff_commands)
            if diff_total == 0:
                continue
                
            diff_mastered = len([
                c.name
                for c in diff_commands
                if c.name in mastered_set
            ])
            
            by_difficulty[difficulty] = {
                "total": diff_total,
                "mastered": diff_mastered,
                "percentage": round(diff_mastered / diff_total * 100, 1) if diff_total > 0 else 0
            }
        
        remaining_commands = [
            cmd for cmd in self.commands.keys() 
            if cmd not in mastered_set
        ]
        
        return {
            "total_commands": total,
            "mastered_commands": mastered,
            "progress_percentage": round(mastered / total * 100, 1) if total > 0 else 0,
            "by_category": by_category,
            "by_difficulty": by_difficulty,
            "remaining_commands": sorted(remaining_commands),
            "mastered_commands_list": sorted([cmd for cmd in mastered_set if cmd in self.commands])
        }
